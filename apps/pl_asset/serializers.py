from rest_framework import serializers
from . import models

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = [
            'slug_name',
            'type',
            'properties',
            'content'
        ]

class RunnableAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RunnableAsset
        fields = ['asset']
