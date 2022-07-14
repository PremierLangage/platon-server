from rest_framework import serializers
from . import models

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = [
            'path',
            'name',
            'type',
            'properties',
            'content'
        ]

class RunnableAssetSerializer(serializers.ModelSerializer):

    path = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    properties = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.RunnableAsset
        fields = [
            'path',
            'name',
            'type',
            'properties',
            'content'
        ]
    
    def get_path(self, value: models.RunnableAsset):
        return value.asset.path

    def get_name(self, value: models.RunnableAsset):
        return value.asset.name

    def get_type(self, value: models.RunnableAsset):
        return value.asset.type
    
    def get_properties(self, value: models.RunnableAsset):
        return value.asset.properties

    def get_content(self, value: models.RunnableAsset):
        return value.get(self.context.get('request'))
