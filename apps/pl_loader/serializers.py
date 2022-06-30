from rest_framework import serializers
from .models import Loader, Publisher



class LoaderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loader
        fields = '__all__'
    

class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = '__all__'