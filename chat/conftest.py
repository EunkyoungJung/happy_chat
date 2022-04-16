import pytest


class MockConsumer:
    def __init__(self, scope, channel_name):
        self.scope = scope
        self.channel_name = channel_name


@pytest.fixture
def mock_scope():
    return {'url_route': {'args': (), 'kwargs': {'room_name': 'test'}}}


@pytest.fixture
def chat_consumer(mock_scope):
    return MockConsumer(mock_scope, 'test')
