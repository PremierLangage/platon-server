import json
from typing import Optional

from common.errors import RestError
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import FileSerializer, ResourceSerializer
from .serializers import CircleSerializer, CircleResourceSerializer
from .models import Circle, File, Resource


class FileList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = FileSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def post(self, request: Request, pk):
        """ create new file"""

        content = request.data.get('content')
        filename = request.data.get('filename')
        if not content:
            return Response(
                RestError('resource/content/missing'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not filename:
            return Response(
                RestError('resource/filename/missing'),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            f = File.create_file(pk, filename, content)
            serializer = FileSerializer(f)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Resource.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )


class FileDetail(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = FileSerializer

    def patch(self, request: Request, pk, fpk):
        """Update a file"""

        content = request.data.get('content')
        if not content:
            return Response(
                RestError('resource/content/missing'),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resource = Resource.objects.get(id=pk)
            f = File.objects.get(id=fpk, resource=resource)
            f.update_file(content)

        except Resource.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )

        except File.DoesNotExist:
            return Response(
                RestError('file/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = FileSerializer(f)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        """return a serialized file"""
        return self.retrieve(request, *args, **kwargs)



class ResourcesList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ResourceDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """View that allow to retrieve the informations of a single resource"""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ResourceTag(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def patch(self, request: Request, pk):
        """Create a new tag"""
        try:
            resource = Resource.objects.get(id=pk)
            resource.tag(pk, path)

        except Resource.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResourceFolder(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def post(self, request: Request, pk):
        """Create a new folder"""
        path = request.data.get('path')
        if not path:
            return Response(
                RestError('resource/pass/missing'),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resource = Resource.objects.get(id=pk)
            resource.create_folder(pk, path)

        except Resource.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request: Request, pk):
        """delete folder and file in folders. `path` is required in request.
        `path`is relative path from git repo to folder """
        path = request.data.get('path')
        if not path:
            return Response(
                RestError('resource/pass/missing'),
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resource = Resource.objects.get(id=pk)
            resource.delete_folder(pk, path)

        except Resource.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(serializer.data, status=status.HTTP_200_OK)


# ====== TODO move in circle activity ==================

class CircleList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request):
        
        id_parent = request.data.get('parent_id')
        path = request.data.get('path')
        name = request.data.get('name')
        description = request.data.get('description')
        tags = request.data.get('tags')

        parent = None
        
        if id_parent is not None:
            parent = Circle.objects.get(id=id_parent)
        
        circle = Circle.objects.create(
            parent=parent, name=name,
            description=description,
            tags=tags,
            path=path
        )
        
        if not circle:
            return Response(
                RestError('circle/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )
        circle.create_resource()
        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CircleDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """View that allow to retrieve the informations of a single circle"""
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer

    @property
    def allowed_methods(self):
        """
        Return the list of allowed HTTP methods, uppercased.
        """
        self.http_method_names.append("patch")
        self.http_method_names.append("put")
        return [method.upper() for method in self.http_method_names
                if hasattr(self, method)]

    def get(self, request: Request, pk):
        return self.retrieve(request, pk=pk)

    def put(self, request: Request, pk):
        """update cirle"""
        return self.update(request, pk=pk)

    def patch(self, request: Request, pk):
        """update resource of circle"""
        # TODO changement de file.
        return self.partial_update(request, pk=pk)


class CircleResourceTree(generics.ListAPIView):
    """retrive all parents of a single Circle"""
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer

    def get_queryset(self):
        queryset = Circle.objects.all()
        tree_id = []
        id_circle = self.request.query_params.get('id_circle', None)
        
        if id_circle is not None:
            tree_id.append(id_circle)
            circle = Circle.objects.get(id=id_circle)
            while(circle and circle.parent):
                circle = circle.parent
                tree_id.append(circle.id)
            
        queryset = queryset.filter(circle__pk__in=tree_id)
        return queryset
