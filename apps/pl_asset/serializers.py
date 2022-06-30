from rest_framework import serializers
from .models import Asset, AssetProperties
from pl_properties.serializers import PropertiesSerializer

class AssetSerializer(serializers.ModelSerializer):
    
    #properties = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Asset
        fields = [
            'id',
            'name',
            #'properties',
            'date_creation',
            'parent',
            'resource',
            'resource_version',
        ]

    def get_properties(self, asset: Asset):
        query_set = AssetProperties.objects.filter(asset=asset)
        properties = dict()
        for asset_property in query_set:
            query = PropertiesSerializer(queryset=property).to_representation(asset_property.property)
            properties[query.get_field_name()] = query.data
        return properties
    


class AssetPropertiesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssetProperties
        fields = '__all__'
