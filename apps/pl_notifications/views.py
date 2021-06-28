from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import models

from pl_core.mixins import CrudViewSet

from .serializers import NotificationSerializer
from .models import Notification

User = get_user_model()

class NotificationViewSet(CrudViewSet):
    
    serializer_class = NotificationSerializer
    
    def get_serializer_class(self):
        # serializer = self.get_serializer(data=self.request.data)
        # serializer.is_valid(raise_exception=True)
        return NotificationSerializer

    def get_queryset(self):
        user: User = self.request.user
        return user.notifications_users.all()

    @classmethod
    def as_detail(cls):
        return cls.as_view({'get': 'retrieve', 'patch': 'partial_update','delete': 'destroy'})