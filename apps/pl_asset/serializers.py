from rest_framework import serializers

from . import models
from pl_users.serializers import UserSerializer

class AssetSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = models.Asset
        fields = (
            'name',
            'type',
            'created_at',
            'updated_at',
            'author'
        )
        read_only_fields = (
            'type',
            'created_at',
            'updated_at',
        )

    def get_author(self, obj):        
        return UserSerializer(
            models.User.objects.get(username=obj.author),
            context={
                'request': self.context['request']
            }
        ).data
