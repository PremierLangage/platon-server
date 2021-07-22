import dgeq
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.core.exceptions import PermissionDenied
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TransactionTestCase
from pl_sandbox.models import Sandbox
from platon.routing import application

User = get_user_model()
SANDBOX_URL = settings.SANDBOX_URL


class ConsumerTestCase(TransactionTestCase):

    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create_user("test")
        self.user.user_permissions.add(Permission.objects.get(codename="view_usage"))
        self.user.user_permissions.add(Permission.objects.get(codename="view_sandboxspecs"))
        self.user.user_permissions.add(Permission.objects.get(codename="view_containerspecs"))
        self.channel_layer = get_channel_layer()


    # async def test_usage_consumer(self):
    #     communicator = WebsocketCommunicator(
    #         application, f'/ws/sandbox/sandbox-usages/{self.sandbox.pk}/'
    #     )# async def test_usage_consumer(self):
    #     communicator = WebsocketCommunicator(
    #         application, f'/ws/sandbox/sandbox-usages/{self.sandbox.pk}/'
    #     )
    #     communicator.scope["user"] = self.user
    #     await communicator.connect()
    #     communicator.scope["user"] = self.user
    #     await communicator.connect()

    #     usage = await self.sandbox.poll_usage()
    #     data = DjangoJSONEncoder().encode(
    #         await database_sync_to_async(dgeq.serialize)(usage)
    #     )
    #     await self.channel_layer.group_send(
    #         f"sandbox_usage_{self.sandbox.pk}",
    #         {
    #             'type':  'sandbox_usage',
    #             'usage': data
    #         }
    #     )
    #     result = await communicator.receive_from()
    #     self.assertEqual(data, result)
    #     await communicator.disconnect()


    # async def test_usage_consumer_permission_denied(self):
    #     with self.assertRaises(PermissionDenied):
    #         communicator = WebsocketCommunicator(
    #             application, f'/ws/sandbox/sandbox-usages/{self.sandbox.pk}/'
    #         )
    #         communicator.scope["user"] = AnonymousUser()
    #         await communicator.connect()


    # async def test_sandbox_specs_consumer(self):
    #     communicator = WebsocketCommunicator(
    #         application, f'/ws/sandbox/sandbox-specs/{self.sandbox.pk}/'
    #     )
    #     communicator.scope["user"] = self.user
    #     await communicator.connect()
    #
    #     sandbox_specs, _ = await self.sandbox.poll_specifications()
    #     data_sandbox_specs = DjangoJSONEncoder().encode(
    #         await database_sync_to_async(dgeq.serialize)(sandbox_specs)
    #     )
    #     await self.channel_layer.group_send(
    #         f"sandbox_sandbox_specs_{self.sandbox.pk}",
    #         {
    #             'type':  'sandbox_specs',
    #             'specs': data_sandbox_specs
    #         }
    #     )
    #     result = await communicator.receive_from()
    #     self.assertEqual(data_sandbox_specs, result)
    #     await communicator.disconnect()


    async def test_sandbox_specs_consumer_permission_denied(self):
        with self.assertRaises(PermissionDenied):
            communicator = WebsocketCommunicator(
                application, f'/ws/sandbox/sandbox-specs/{self.sandbox.pk}/'
            )
            communicator.scope["user"] = AnonymousUser()
            await communicator.connect()


    # async def test_container_specs_consumer(self):
    #     communicator = WebsocketCommunicator(
    #         application, f'/ws/sandbox/container-specs/{self.sandbox.pk}/'
    #     )
    #     communicator.scope["user"] = self.user
    #     await communicator.connect()

    #     _, container_specs = await self.sandbox.poll_specifications()
    #     data_container_specs = DjangoJSONEncoder().encode(
    #         await database_sync_to_async(dgeq.serialize)(container_specs)
    #     )
    #     await self.channel_layer.group_send(
    #         f"sandbox_container_specs_{self.sandbox.pk}",
    #         {
    #             'type':  'container_specs',
    #             'specs': data_container_specs
    #         }
    #     )
    #     result = await communicator.receive_from()
    #     self.assertEqual(data_container_specs, result)
    #     await communicator.disconnect()


    async def test_container_specs_consumer_permission_denied(self):
        with self.assertRaises(PermissionDenied):
            communicator = WebsocketCommunicator(
                application, f'/ws/sandbox/container-specs/{self.sandbox.pk}/'
            )
            communicator.scope["user"] = AnonymousUser()
            await communicator.connect()
