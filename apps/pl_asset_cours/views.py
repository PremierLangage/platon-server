from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from pl_core.mixins import CrudViewSet

from pl_asset_cours.models import AssetCours, AssetCoursSession
from pl_asset_cours.serializers import AssetCoursSerializer, AssetCoursDetailSeralizer, AssetCoursSessionSerializer

class AssetCoursViewSet(CrudViewSet):

    lookup_field = 'name'
    lookup_url_kwarg = 'name'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    serializer_classes = {
        'list': AssetCoursSerializer,
        'create': AssetCoursSerializer,
        'retrieve': AssetCoursDetailSeralizer,
        'patch': AssetCoursDetailSeralizer,
        'partial_update': AssetCoursDetailSeralizer,
        'destroy': AssetCoursSerializer
    }

    default_serializer_class = AssetCoursDetailSeralizer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def get_queryset(self):
        return AssetCours.objects.all()


class AssetCoursSessionViewSet(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = AssetCoursSessionSerializer

    def get(self, request, *args, **kwargs):
        try:
            asset = AssetCours.objects.get(name=kwargs.get('name'))
        except AssetCours.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        (session, flag) = AssetCoursSession.objects.get_or_create(
            asset=asset,
            user=request.user
        )
        serializer = AssetCoursSessionSerializer(session)
        return Response(serializer.data)

    @classmethod
    def as_play(cls):
        return cls.as_view({'get': 'get'})