from rest_framework import response, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from pl_core.mixins import CrudViewSet

from .import serializers, models, enums

# Create your views here.
class AssetViewSet(CrudViewSet):
    
    lookup_field = 'path'
    serializer_class = serializers.AssetSerializer

    # Devloppement settings
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return models.Asset.objects.all()

class UserAssetViewSet(CrudViewSet):

    serializer_class = serializers.AssetSerializer

    # Devloppement settings
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return models.Asset.objects.filter(type=enums.AssetType.COURS)

class RunnableAssetViewSet(CrudViewSet):

    lookup_field = 'asset'
    serializer_class = serializers.RunnableAssetSerializer

    # Devloppement settings
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return models.RunnableAsset.objects.all()
