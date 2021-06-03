from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import models

from pl_core.mixins import CrudViewSet

from .serializers import NotificationSerializer
from .models import Notification



class NotificationViewSet(CrudViewSet):
    def get_serializer_class(self):
        return NotificationSerializer

    def get_queryset(self):
        return Notification.list_all()