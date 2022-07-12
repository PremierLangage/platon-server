from rest_framework import response, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from pl_core.mixins import CrudViewSet

from .import serializers, models

# Create your views here.
class AssetViewSet(CrudViewSet):
    
    lookup_field = 'slug_name'
    serializer_class = serializers.AssetSerializer

    # Devloppement settings
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return models.Asset.objects.all()

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
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if bool(request.user and request.user.is_authenticated):
            (session, flag) = models.RunnableAssetSession.objects.get_or_create(asset=asset, user=request.user)
            print('#################')
            print(session.build())
            print('#################')

        return Response({'test_build': 'OK'})

    def post(self, request, *args, **kwargs):
        return Response({'test_eval': 'OK'})

    @classmethod
    def as_detail(cls):
        return cls.as_view({'get': 'get', 'post': 'post'})