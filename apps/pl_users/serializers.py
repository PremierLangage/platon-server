from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    circles_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name',
            'last_name', 'is_editor', 'is_admin',
            'avatar', 'url', 'circles_url'
        )

    def get_url(self, value):
        request = self.context['request']
        return reverse(
            'pl_users:user-detail',
            request=request,
            kwargs={'username': value.username}
        )

    def get_circles_url(self, value):
        request = self.context['request']
        url = reverse(
            'pl_resources:circle-list',
            request=request,
        )
        return f'{url}?member={value.username}'
