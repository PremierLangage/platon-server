from rest_framework import serializers
from . import models

class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Asset
        fields = '__all__'

class RunnableAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.RunnableAsset
        fields = '__all__'
