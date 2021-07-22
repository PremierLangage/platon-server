from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.state import User
from rest_framework_simplejwt.tokens import UntypedToken


@database_sync_to_async
def get_user(validated_token):
    try:
        return get_user_model().objects.get(id=validated_token["user_id"])
    except User.DoesNotExist:
        return AnonymousUser()


# https://hashnode.com/post/using-django-drf-jwt-authentication-with-django-channels-cjzy5ffqs0013rus1yb9huxvl

class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
       # Close old database connections to prevent usage of timed out connections
        close_old_connections()
        headers = dict(scope["headers"])
        if b'authorization' not in headers:
            scope['user'] = AnonymousUser()
            return await super().__call__(scope, receive, send)

        try:
            token = headers[b'authorization'].decode().split().pop()
            UntypedToken(token)
        except (InvalidToken, TokenError):
            scope['user'] = AnonymousUser()
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            scope['user'] = await get_user(decoded_data)

        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
