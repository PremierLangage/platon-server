import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import PermissionDenied


#todo
class NotificationConsumer(AsyncWebsocketConsumer):
    """ Allow to send notification with websocket """
    
    notification_group_name: str
    # sandbox_id: int

    
    async def connect(self):
        """Connect this consumer."""
        # self.notification_group_name = self.scope["user"].username
        self.notification_group_name = self.scope['url_route']['kwargs']['user']
        print(self.scope)
        
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': self.notification_group_name
        }))


    async def notification_message(self, event):
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'message': message
        }))