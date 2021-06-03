from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Notification

User = get_user_model()


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    
    class Meta:
        model = Notification
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