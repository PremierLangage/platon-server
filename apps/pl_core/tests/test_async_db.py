from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from pl_core import async_db



class HasPermAsyncTestCase(TransactionTestCase):
    
    async def test_ok(self):
        superuser = await database_sync_to_async(User.objects.create_user)(
            "superuser", is_superuser=True
        )
        user = await database_sync_to_async(User.objects.create_user)("user")
        
        self.assertTrue(await async_db.has_perm_async(superuser, "pl_sandbox:view_usage"))
        self.assertFalse(await async_db.has_perm_async(user, "pl_sandbox:view_usage"))
