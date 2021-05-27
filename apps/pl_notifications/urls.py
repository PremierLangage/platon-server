from django.urls import path, re_path

from . import consumers, views

# urlpatterns = [
#     path('notifications/', views.NotificationView.as_view(), name='notification-list'),
#     path('notifications/<int:pk>/', views.NotificationView.as_view(), name='notification-detail'),
    
# ]

# websocket_urlpatterns = [
#     re_path(r'ws/notifications/(?P<user>\w+)/$', consumers.NotificationConsumer.as_asgi()),
# ]