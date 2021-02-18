from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='profile.role', read_only=True)
    isAdmin = serializers.BooleanField(source='profile.is_admin', read_only=True)
    userName = serializers.CharField(source='username', read_only=True)
    lastName = serializers.CharField(source='last_name', read_only=True)
    firstName = serializers.CharField(source='first_name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'userName', 'email', 'firstName', 'lastName', 'role', 'isAdmin')
