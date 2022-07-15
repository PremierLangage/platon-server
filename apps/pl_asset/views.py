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

    def get(self, request, *args, **kwargs):

        try:
            asset = models.RunnableAsset.objects.get(asset=kwargs.get('asset'))
        except models.RunnableAsset.DoesNotExist:
            return Response({"detail": "Pas trouvé."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "path": asset.asset.path,
            "name": asset.asset.name,
            "type": asset.asset.type,
            "properties": asset.asset.properties,
            "content": asset.content(request, kwargs)
        })
        

    @classmethod
    def as_detail(cls):
        return cls.as_view({'get':'get'})
