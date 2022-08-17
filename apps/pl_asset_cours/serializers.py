from rest_framework import serializers

from pl_asset.serializers import AssetSerializer

from . import models

class AssetCoursSerializer(AssetSerializer):

    class Meta(AssetSerializer.Meta):
        model = models.AssetCours
        fields = AssetSerializer.Meta.fields
    
    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        asset = models.AssetCours.objects.create(**validated_data)
        return asset

class AssetCoursDetailSeralizer(AssetSerializer):

    class Meta(AssetSerializer.Meta):
        model = models.AssetCours
        fields = AssetSerializer.Meta.fields + (
            'description',
            'properties',
            'content',
        )
    
class AssetCoursSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AssetCoursSession
        fields = '__all__'