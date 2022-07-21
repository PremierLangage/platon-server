import json

from rest_framework import serializers

from .loader import Loader

class LiveAssetSerializer(serializers.Serializer):

    path = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    properties = serializers.SerializerMethodField(read_only=True)
    content = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = [
            'path',
            'name',
            'type',
            'properties',
            'content'
        ]
    
    def get_path(self, value: Loader):
        return str(value.resource.name) + '/' + str(value.environment)
    
    def get_name(self, value: Loader):
        return value.resource.name
    
    def get_type(self, value: Loader):
        return value.resource.type
    
    def get_properties(self, value: Loader):
        return {}

    def get_content(self, value: Loader):
        return json.loads(value.build_request.response.result)