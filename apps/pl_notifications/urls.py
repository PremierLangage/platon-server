from django.urls import path, re_path

from .views import NotificationViewSet
from .consumers import NotificationConsumer

app_name = 'pl_notifications'

urlpatterns = [
    path('notifications/', NotificationViewSet.as_list(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationViewSet.as_detail(), name='notification-detail'),   
]

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/notifications/(?P<user>\w+)/$', NotificationConsumer.as_asgi()),
]