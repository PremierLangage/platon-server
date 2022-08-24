from rest_framework import serializers

from .models import Asset, AssetActivity, AssetCours, AssetExersice

class AssetSerializer(serializers.ModelSerializer):

    author = serializers.CharField(read_only=True, source='author.username')
    path = serializers.CharField(read_only=True)

    class Meta:
        model = Asset
        fields = (
            'name',
            'type',
            'created_at',
            'updated_at',
            'author',
            'parent',
            'path'
        )

class AssetCoursSerializer(serializers.ModelSerializer):

    asset = serializers.CharField(read_only=True, source='asset.name')
    asset = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AssetCours
        fields = (
            'asset',
            'description',
            'content'
        )
    
    def get_asset(self, value: AssetCours):
        return AssetSerializer(value.asset).data

class AssetActivitySerializer(serializers.ModelSerializer):

    asset = serializers.CharField(read_only=True, source='asset.name')

    class Meta:
        model = AssetActivity
        fields = (
            'asset',
            'content'
        )

class AssetExersiceSerializer(serializers.ModelSerializer):

    asset = serializers.CharField(read_only=True, source='asset.name')

    class Meta:
        model = AssetExersice
        fields = (
            'asset',
            'content'
        )