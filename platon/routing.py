from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from pl_sandbox import urls as pl_sandbox_url
from pl_notifications import urls as pl_notifications_url


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            pl_sandbox_url.websocket_urlpatterns + 
            pl_notifications_url.websocket_urlpatterns
        )
    ),
})
