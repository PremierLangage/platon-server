from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.exceptions import PermissionDenied

from pl_core.async_db import has_perm_async



class SandboxUsageConsumer(AsyncWebsocketConsumer):
    """Allow to automatically receive the last polled Sandbox's Usage."""
    
    sandbox_id: int
    sandbox_group_name: str
    
    
    async def connect(self):
        """Connect this consumer."""
        if not await has_perm_async(self.scope["user"], "pl_sandbox.view_usage"):
            raise PermissionDenied()
        
        self.sandbox_id = self.scope['url_route']['kwargs']['pk']
        self.sandbox_group_name = 'sandbox_usage_%s' % self.sandbox_id
        
        await self.channel_layer.group_add(
            self.sandbox_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    
    async def disconnect(self, close_code):
        """Disconnect this consumer."""
        await self.channel_layer.group_discard(
            self.sandbox_group_name,
            self.channel_name
        )
    
    
    async def sandbox_usage(self, event):
        """Send usage to connected consumer."""
        await self.send(text_data=event['usage'])



class SandboxSpecsConsumer(AsyncWebsocketConsumer):
    """Allow to automatically receive the last polled SandboxSpecification."""
    
    sandbox_id: int
    sandbox_group_name: str
    
    
    async def connect(self):
        """Connect this consumer."""
        if not await has_perm_async(self.scope["user"], "pl_sandbox.view_sandboxspecs"):
            raise PermissionDenied()
        
        self.sandbox_id = self.scope['url_route']['kwargs']['pk']
        self.sandbox_group_name = 'sandbox_sandbox_specs_%s' % self.sandbox_id
        
        await self.channel_layer.group_add(
            self.sandbox_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    
    async def disconnect(self, close_code):
        """Disconnect this consumer."""
        await self.channel_layer.group_discard(
            self.sandbox_group_name,
            self.channel_name
        )
    
    
    async def sandbox_specs(self, event):
        """Send sandbox specifications to connected consumer."""
        await self.send(text_data=event['specs'])



class ContainerSpecsConsumer(AsyncWebsocketConsumer):
    """Allow to automatically receive the last polled ContainerSpecification."""
    sandbox_id: int
    sandbox_group_name: str
    
    
    async def connect(self):
        """Connect this consumer."""
        if not await has_perm_async(self.scope["user"], "pl_sandbox.view_containerspecs"):
            raise PermissionDenied()
        
        self.sandbox_id = self.scope['url_route']['kwargs']['pk']
        self.sandbox_group_name = 'sandbox_container_specs_%s' % self.sandbox_id
        
        await self.channel_layer.group_add(
            self.sandbox_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    
    async def disconnect(self, close_code):
        """Disconnect this consumer."""
        await self.channel_layer.group_discard(
            self.sandbox_group_name,
            self.channel_name
        )
    
    
    async def container_specs(self, event):
        """Send container specifications to connected consumer."""
        await self.send(text_data=event['specs'])
