from django.urls import path, re_path

from . import consumers, views

# websocket_urlpatterns = [
    # re_path(r'ws/sandbox/notifications/(?P<pk>\d+)/$', consumers.NotificationConsumer.as_asgi()),
# ]