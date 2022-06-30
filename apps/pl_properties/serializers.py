from dataclasses import field
from rest_framework import serializers
from .models import DescriptionProperty


class DescriptionPropertySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DescriptionProperty
        fields = '__all__'
    
    def get_field_name(self):
        return 'description'


class PropertiesSerializer(serializers.RelatedField):
    
    def to_representation(self, value):
        if isinstance(value, DescriptionProperty):
            return DescriptionPropertySerializer(value)
        raise Exception('Unexpected type of tagged object')