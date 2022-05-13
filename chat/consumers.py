# chat/consumers.py
import json
from unicodedata import name
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import User, Room, Message

# map(['127.0.0.1', 49995], lambda item: str(item))

class ChatController:
    def __init__(self, consumer):
        # print("ChatController__init__, jek", dir(consumer))
        # print("ChatController__init__, jek", consumer['scope'])
        self.consumer = consumer

    def get_user_name(self):
        return ":".join(map(lambda item: str(item), self.consumer.scope.get('client')))
    
    def get_or_create_user(self):
        return User.objects.get_or_create(username=self.get_user_name())[0]

    def get_or_create_room(self):
        return Room.objects.get_or_create(name=self.get_room_name())[0]

    def get_room_name(self):
        return self.consumer.scope['url_route']['kwargs']['room_name']

    def get_room_group_name(self):
        return 'chat_{}'.format(self.get_room_name())

    def join_room_group(self):
        async_to_sync(self.consumer.channel_layer.group_add)(
            self.get_room_group_name(), 
            self.consumer.channel_name
        )
        # print("ChatController join_room_group, jek", dir(self.consumer))
        # print("ChatController join_room_group, jek", self.consumer.scope)
        # print("ChatController join_room_group, jek!", self.consumer.scope.get('client'))
        # create_user(email = email, name = name, phone = phone, password = password)
        self.get_or_create_user()
        self.get_or_create_room()
        self.consumer.accept()

    def leave_room_group(self):
        async_to_sync(self.consumer.channel_layer.group_discard)(
            self.get_room_group_name(),
            self.consumer.channel_name
        )
    
    def send_msg_to_room_group(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        sender = self.get_or_create_user()
        room = self.get_or_create_room()

        Message.objects.create(
            sender=sender,
            room=room,
            content=message,
        )
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
