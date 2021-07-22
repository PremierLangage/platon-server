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
