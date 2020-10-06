import os

from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TransactionTestCase
from django_celery_beat.models import PeriodicTask

from django_sandbox.exceptions import SandboxDisabledError
from django_sandbox.models import ContainerSpecs, Sandbox, SandboxSpecs, Usage


SANDBOX_URL = settings.SANDBOX_URL

TEST_DATA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_data")



class SandboxModelTests(TransactionTestCase):
    
    def setUp(self):
        self.sandbox = Sandbox.objects.create(name="Test", url=SANDBOX_URL, enabled=True)
        self.user = User.objects.create(username="user", password="password")
    
    
    async def test_create_periodic_tasks(self):
        self.assertEquals(
            2,
            await database_sync_to_async(PeriodicTask.objects.count)(),
        )
        await database_sync_to_async(Sandbox.objects.create)(
            name="Test2", url="http://localhost:7001/", enabled=True
        )
        self.assertEquals(
            4,
            await database_sync_to_async(PeriodicTask.objects.count)()
        )
    
    
    async def test_poll_specifications(self):
        host, container = await self.sandbox.poll_specifications()
        self.assertTrue(isinstance(host, SandboxSpecs))
        self.assertTrue(isinstance(container, ContainerSpecs))
    
    
    async def test_poll_specifications_disable(self):
        self.sandbox.enabled = False
        await database_sync_to_async(self.sandbox.save)()
        await database_sync_to_async(self.sandbox.refresh_from_db)()
        with self.assertRaises(SandboxDisabledError):
            await self.sandbox.poll_specifications()
    
    
    async def test_poll_usage(self):
        usage = await self.sandbox.poll_usage()
        self.assertEquals(type(usage), Usage)
        self.assertEquals(usage.enabled, True)
        
        sandbox = await database_sync_to_async(Sandbox.objects.create)(
            name="Test2", url="http://localhost:7001/", enabled=False
        )
        usage = await sandbox.poll_usage()
        self.assertEquals(type(usage), Usage)
        self.assertEquals(usage.enabled, False)
    
    
    async def test_execute(self):
        config = {
            'commands':    ['echo "test" > result.txt', 'echo "test2"'],
            'result_path': 'result.txt'
        }
        
        request = await self.sandbox.execute(user=self.user, config=config)
        self.assertTrue(request.success)
        self.assertDictEqual(config, request.config)
    
    
    async def test_execute_disable(self):
        config = {
            'commands':    ['echo "test" > result.txt', 'echo "test2"'],
            'result_path': 'result.txt'
        }
        
        self.sandbox.enabled = False
        await database_sync_to_async(self.sandbox.save)()
        await database_sync_to_async(self.sandbox.refresh_from_db)()
        request = await self.sandbox.execute(user=self.user, config=config)
        self.assertFalse(request.success)
        self.assertDictEqual(config, request.config)
        self.assertIn(SandboxDisabledError.__name__, request.traceback)
    
    
    async def test_retrieve_file(self):
        config = {
            'commands': ['echo "test" > result.txt', 'echo "test2"'],
            'save':     True
        }
        
        request = await self.sandbox.execute(user=self.user, config=config)
        self.assertTrue(request.success)
        env = await self.sandbox.retrieve(
            environment=request.response.environment, file="result.txt"
        )
        self.assertEqual(env.read(), b"test\n")
    
    
    async def test_retrieve_disabled(self):
        self.sandbox.enabled = False
        await database_sync_to_async(self.sandbox.save)()
        await database_sync_to_async(self.sandbox.refresh_from_db)()
        with self.assertRaises(SandboxDisabledError):
            await self.sandbox.retrieve("unknown")
