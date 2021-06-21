from channels.routing import ProtocolTypeRouter, URLRouter
from pl_notifications import urls as pl_notifications_url
from pl_sandbox import urls as pl_sandbox_url

from .auth_middleware import JwtAuthMiddleware

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket":  JwtAuthMiddleware(
        URLRouter(
            pl_sandbox_url.websocket_urlpatterns
            + pl_notifications_url.websocket_urlpatterns
        )
    ),
})
