import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import PermissionDenied
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationConsumer(AsyncWebsocketConsumer):
    """ Allow to send notification with websocket """

    group_name: str

    async def connect(self):
        """Connect this consumer."""
        self.user = self.scope['user']
        # TODO refuse non logged user (anonymous)
        self.group_name = self.user.username
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notification_available(self, event):
        print('OKOK')
        await self.send(text_data=json.dumps(event))


def send_notification(username: str, unreaded=1):
    channel_layer = get_channel_layer()
    group_send = async_to_sync(channel_layer.group_send)
    group_send(username, {
        "type": "notification.available",
        "unreaded": unreaded,
    })
