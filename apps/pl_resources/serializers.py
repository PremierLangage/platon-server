from .models import Circle, Resource, File
from rest_framework import serializers


class CircleResourceSerializer(serializers.ModelSerializer):
    
    files = serializers.StringRelatedField(many=True)

    class Meta:
        model = Circle
        fields = ('id', 'name', 'path', 'description', 'files')


class CircleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Circle
        fields = ('id', 'name', 'path', 'description')


class ResourceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Resource
        fields = ('id', 'name', 'path', 'description')


class FileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = File
        fields = ('id', 'resource')
