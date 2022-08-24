from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from pl_asset.types import AssetType
from pl_core.mixins import CrudViewSet

from .serializers import AssetActivitySerializer, AssetExersiceSerializer, AssetSerializer, AssetCoursSerializer
from .models import Asset, AssetActivity, AssetCours, AssetExersice
from .types import AssetType


# DEFAULT ASSET
class AssetViewSet(CrudViewSet):

    lookup_field = 'path'
    lookup_url_kwarg = 'path'
    serializer_class = AssetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Asset.objects.all()

# ASSET COURS
class AssetCoursViewSet(CrudViewSet):

    serializer_class = AssetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Asset.objects.filter(type=AssetType.COURS)

class AssetCoursDetailViewSet(CrudViewSet):

    lookup_field = 'asset'
    lookup_url_kwarg = 'name'
    serializer_class = AssetCoursSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return AssetCours.objects.all()
    
    def get(self, request, *args, **kwargs):
        try:
            asset = Asset.objects.get(
                name=kwargs.get(self.lookup_url_kwarg),
                type=AssetType.COURS
            )
        except Asset.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        (asset_cours, flag) = AssetCours.objects.get_or_create(asset=asset)
        serializer = AssetCoursSerializer(asset_cours)
        return Response(serializer.data)
    
    @classmethod
    def as_detail(cls):
        return cls.as_view({
            'get': 'get',
            'patch': 'partial_update'
        })


# ASSET ACTIVITY
class AssetActivityViewSet(CrudViewSet):

    serializer_class = AssetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Asset.objects.filter(type=AssetType.ACTIVITY)

class AssetActivityDetailViewSet(CrudViewSet):

    lookup_field = 'asset'
    lookup_url_kwarg = 'name'
    serializer_class = AssetActivitySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return AssetActivity.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            asset = Asset.objects.get(
                name=kwargs.get(self.lookup_url_kwarg),
                type=AssetType.ACTIVITY
            )
        except Asset.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        (asset_activity, flag) = AssetActivity.objects.get_or_create(asset=asset)
        serializer = AssetActivitySerializer(asset_activity)
        return Response(serializer.data)
    
    @classmethod
    def as_detail(cls):
        return cls.as_view({
            'get': 'get',
            'patch': 'partial_update'
        })

# ASSET EXERSICE
class AssetExersiceViewSet(CrudViewSet):

    serializer_class = AssetSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Asset.objects.filter(type=AssetType.EXERCISE)

class AssetExersiceDetailViewSet(CrudViewSet):

    lookup_field = 'asset'
    lookup_url_kwarg = 'name'
    serializer_class = AssetExersiceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return AssetExersice.objects.all()
    
    def get(self, request, *args, **kwargs):
        try:
            asset = Asset.objects.get(
                name=kwargs.get(self.lookup_url_kwarg),
                type=AssetType.EXERCISE
            )
        except Asset.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        (asset_exersice, flag) = AssetExersice.objects.get_or_create(asset=asset)
        serializer = AssetExersiceSerializer(asset_exersice)
        return Response(serializer.data)
    
    @classmethod
    def as_detail(cls):
        return cls.as_view({
            'get': 'get',
            'patch': 'partial_update'
        })