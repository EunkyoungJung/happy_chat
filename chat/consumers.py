# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatController:
    def __init__(self, consumer):
        self.consumer = consumer
    
    def get_room_name(self):
        return self.consumer.scope['url_route']['kwargs']['room_name']

    def get_room_group_name(self):
        return 'chat_{}'.format(self.get_room_name())

    def join_room_group(self):
        async_to_sync(self.consumer.channel_layer.group_add)(
            self.get_room_group_name(), 
            self.consumer.channel_name
        )
        self.consumer.accept()

    def leave_room_group(self):
        async_to_sync(self.consumer.channel_layer.group_discard)(
            self.get_room_group_name(),
            self.consumer.channel_name
        )
    
    def send_msg_to_room_group(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.consumer.channel_layer.group_send)(
            self.get_room_group_name(),
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    def broadcast_msg_to_room_group(self, event):
        message = event['message']
        self.consumer.send(text_data=json.dumps({
            'message': message
        }))


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = ChatController(self)

    def connect(self):
        self.controller.join_room_group()

    def disconnect(self, close_code):
        self.controller.leave_room_group()

    def receive(self, text_data):
        self.controller.send_msg_to_room_group(text_data)

    def chat_message(self, event):
        self.controller.broadcast_msg_to_room_group(event)
