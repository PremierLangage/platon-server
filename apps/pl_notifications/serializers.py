from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.reverse import reverse

from . import models

class NotificationSerializer(serializers.ModelSerializer):
    references = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.Notification
        fields = '__all__'