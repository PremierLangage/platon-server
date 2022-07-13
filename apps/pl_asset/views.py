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

    # def create(self, request, *args, **kwargs):
    #     asset_data = request.data

    #     resource = Resource.objects.filter(id=asset_data['resource']).get()
        
    #     directory = 'resource:' + str(asset_data['resource'])
        
    #     version = 'master'
    #     if not not asset_data['resource_version']:
    #         version = asset_data['resource_version']    

    #     loader = Loader.get_loader(request, directory, version)

    #     publisher = Publisher.get_publisher(request, directory, version, loader)
    #     publisher.build(request)
    #     publisher.publish(request, version)
        
    #     parent = None
    #     if 'parent' in asset_data:
    #         parent = asset_data['parent']

    #     asset = models.Asset(
    #         name = asset_data['name'],
    #         parent = parent,
    #         resource = resource,
    #         resource_version = version,
    #         frozen = publisher
    #     )

    #     asset.save()

    #     serializer = serializers.AssetSerializer(asset)
    #     return Response(serializer.data)
        
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
