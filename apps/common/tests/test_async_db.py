from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from common import async_db



class HasPermAsyncTestCase(TransactionTestCase):
    
    async def test_ok(self):
        superuser = await database_sync_to_async(User.objects.create_user)(
            "superuser", is_superuser=True
        )
        user = await database_sync_to_async(User.objects.create_user)("user")
        
        self.assertTrue(await async_db.has_perm_async(superuser, "django_sandbox:view_usage"))
        self.assertFalse(await async_db.has_perm_async(user, "django_sandbox:view_usage"))
