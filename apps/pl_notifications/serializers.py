from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers

from . import models

class NotificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Notification
        fields = '__all__'
        
    

# class NotificationCreateSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = models.Notification
#         fields = '__all__'
        
#     def save(self, **kwargs):
#         request = self.context['request']
#         instance = super().save(
#             author=request.user,
#             status=ResourceStatus.DRAFT
#         )
#         Notification.create(instance.pk, request.user)
#         return instance    