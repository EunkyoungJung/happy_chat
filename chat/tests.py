from chat.consumers import ChatController


def test_dummy():
    assert True


class TestChatConsumer:
    def test_get_room_name(self, chat_consumer):
        cc = ChatController(chat_consumer)
        assert cc.get_room_name() == "test"
    
    def test_get_room_group_name(self, chat_consumer):
        cc = ChatController(chat_consumer)
        assert cc.get_room_group_name() == "chat_test"
