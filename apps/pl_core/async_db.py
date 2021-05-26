from typing import Awaitable

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

User = get_user_model()



@database_sync_to_async
def has_perm_async(user: User, permission: str) -> Awaitable[bool]:
    """Asynchronously check if a `User` has a the given permission."""
    return user.has_perm(permission)
