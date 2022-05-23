from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from pl_core.mixins import CrudViewSet
from pl_loader.models import Publisher, Loader
from pl_resources.models import Resource
from . import models, serializers

class AssetViewSet(CrudViewSet):
    
    lookup_field = 'pk'

    permission_classes = (AllowAny,)
    serializer_class = serializers.AssetSerializer

    def get_queryset(self):
        return models.Asset.objects.all()

    def create(self, request, *args, **kwargs):
        asset_data = request.data

        resource = Resource.objects.filter(id=asset_data['resource']).get()
        
        directory = 'resource:' + str(asset_data['resource'])
        
        version = 'master'
        if not not asset_data['resource_version']:
            version = asset_data['resource_version']    

        loader = Loader.get_loader(request, directory, version)

        publisher = Publisher.get_publisher(request, directory, version, loader)
        publisher.build(request)
        publisher.publish(request, version)
        
        parent = None
        if 'parent' in asset_data:
            parent = asset_data['parent']

        asset = models.Asset(
            name = asset_data['name'],
            parent = parent,
            resource = resource,
            resource_version = version,
            frozen = publisher
        )

        asset.save()

        serializer = serializers.AssetSerializer(asset)
        return Response(serializer.data)
        
        
class AssetPropertiesViewSet(CrudViewSet):
    
    lookup_field = 'asset'

    permission_classes = (AllowAny,)
    serializer_class = serializers.AssetPropertiesSerializer

    def get_queryset(self):
        return models.AssetProperties.objects.all()