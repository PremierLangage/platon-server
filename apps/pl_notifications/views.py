from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import models

from pl_core.mixins import CrudViewSet

from .serializers import NotificationSerializer
from .models import Notification



class NotificationViewSet(CrudViewSet):
    
    serializer_class = NotificationSerializer
    
    def get_serializer_class(self):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return NotificationSerializer

    def get_queryset(self):
        return Notification.list_all()