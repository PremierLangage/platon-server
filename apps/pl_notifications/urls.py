from django.urls import path, re_path

from . import views

app_name = 'pl_notifications'

urlpatterns = [
    path('notifications/', views.NotificationViewSet.as_list(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationViewSet.as_detail(), name='notification-detail'),   
]

# websocket_urlpatterns = [
#     re_path(r'ws/notifications/(?P<user>\w+)/$', consumers.NotificationConsumer.as_asgi()),
# ]