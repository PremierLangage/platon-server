import os
from typing import BinaryIO

from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django_celery_beat.models import PeriodicTask

from django_sandbox.models import Sandbox, SandboxSpecs, ContainerSpecs, Usage, Request, Response

SANDBOX_URL = os.environ.get("SANDBOX_URL", "http://localhost:7000/")

TEST_DATA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")

class SandboxModelTests(TransactionTestCase):
    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create(username="user", password="password")


    def test_create_periodic_tasks(self):
        self.assertEquals(PeriodicTask.objects.count(), 2, True)
        Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.assertEquals(PeriodicTask.objects.count(), 4, True)


    async def test_poll_specifications(self):
        host, container = await self.sandbox.poll_specifications()
        self.assertEquals(type(host), SandboxSpecs, True)
        self.assertEquals(type(container), ContainerSpecs, True)


    async def test_poll_usage(self):
        usage = await self.sandbox.poll_usage()
        self.assertEquals(type(usage), Usage, True)
        self.assertEquals(usage.enabled, True, True)

        sandbox = await database_sync_to_async(Sandbox.objects.create)(name="Test", url=SANDBOX_URL, enabled=False)
        usage = await sandbox.poll_usage()

        self.assertEquals(type(usage), Usage, True)
        self.assertEquals(usage.enabled, False, True)


    async def test_execute(self):
        with open(os.path.join(TEST_DATA_ROOT, "config")) as config_file:
            config = config_file.read()

        with open(os.path.join(TEST_DATA_ROOT, "env")) as env_file:
            env = env_file.read()

        config_file.close()
        env_file.close()

        request = await self.sandbox.execute(user=self.user, config=config, environment=env)
        self.assertEquals(type(request), Request, True)
        self.assertEquals(await database_sync_to_async(Request.objects.count)(), 1, True)

