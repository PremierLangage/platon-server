from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django_sandbox import urls as django_sandbox_url


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            django_sandbox_url.websocket_urlpatterns
        )
    ),
})
