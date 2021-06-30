from django.test import TestCase
from channels.testing import WebsocketCommunicator
from .consumers import NotificationConsumer


class NotificationTests(TestCase):
    async def test_notification_consumer(self):
        communicator = WebsocketCommunicator(NotificationConsumer.as_asgi(), "/notifications/")
        connected, subprotocol = await communicator.connect()
        await communicator.send_to(text_data="hello")
        response = await communicator.receive_from()
        assert response == "hello"
        # Close
        await communicator.disconnect()
