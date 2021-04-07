import json
import os

import dgeq
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TransactionTestCase

from pl_sandbox import tasks
from pl_sandbox.models import ContainerSpecs, Sandbox, SandboxSpecs, Usage
from platon.routing import application


SANDBOX_URL = settings.SANDBOX_URL


class TaskTestCase(TransactionTestCase):
    
    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create_user("test")
        self.user.user_permissions.add(Permission.objects.get(codename="view_usage"))
        self.user.user_permissions.add(Permission.objects.get(codename="view_sandboxspecs"))
        self.user.user_permissions.add(Permission.objects.get(codename="view_containerspecs"))
    
    """ TODO
    async def test_poll_usage(self):
        communicator = WebsocketCommunicator(
            application, f'/ws/sandbox/usage/{self.sandbox.pk}/'
        )
        communicator.scope["user"] = self.user
        await communicator.connect()
        
        await database_sync_to_async(tasks.poll_usage)(self.sandbox.pk)
        result = await communicator.receive_json_from()
        expected = await database_sync_to_async(Usage.objects.all().latest)()
        expected = DjangoJSONEncoder().encode(
            await database_sync_to_async(dgeq.serialize)(expected)
        )
        self.assertDictEqual(json.loads(expected), result)
        await communicator.disconnect()
    """
    
    async def test_poll_specifications(self):
        sandbox_specs_communicator = WebsocketCommunicator(
            application, f'/ws/sandbox/sandbox_specs/{self.sandbox.pk}/'
        )
        sandbox_specs_communicator.scope["user"] = self.user
        container_specs_communicator = WebsocketCommunicator(
            application, f'/ws/sandbox/container_specs/{self.sandbox.pk}/'
        )
        container_specs_communicator.scope["user"] = self.user
        
        await sandbox_specs_communicator.connect()
        await container_specs_communicator.connect()
        await database_sync_to_async(tasks.poll_specifications)(self.sandbox.pk)
        
        expected_sandbox_specs = await database_sync_to_async(SandboxSpecs.objects.get)(
            sandbox=self.sandbox
        )
        expected_sandbox_specs = DjangoJSONEncoder().encode(
            await database_sync_to_async(dgeq.serialize)(expected_sandbox_specs)
        )
        result_sandbox_specs = await sandbox_specs_communicator.receive_json_from()
        self.assertDictEqual(json.loads(expected_sandbox_specs), result_sandbox_specs)
        
        expected_container_specs = await database_sync_to_async(ContainerSpecs.objects.get)(
            sandbox=self.sandbox
        )
        expected_container_specs = DjangoJSONEncoder().encode(
            await database_sync_to_async(dgeq.serialize)(expected_container_specs)
        )
        result_container_specs = await container_specs_communicator.receive_json_from()
        self.assertDictEqual(json.loads(expected_container_specs), result_container_specs)
        
        await container_specs_communicator.disconnect()
        await sandbox_specs_communicator.disconnect()
