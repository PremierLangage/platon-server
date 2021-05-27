from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db import models
from . import serializers

from pl_core.mixins import CrudViewSet



class NotificationViewSet(CrudViewSet):
    
    def get_queryset(self):
        return models.Notification.list_all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.NotificationCreateSerializer
        return serializers.NotificationSerializer