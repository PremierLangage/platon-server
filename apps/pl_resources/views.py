import json
from typing import Optional

from common.errors import RestError
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CircleSerializer, CircleResourceSerializer
from .models import Circle


class FileList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def post(self, request: Request):
        """ create new file"""
        # TODO faire la méthode
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
                status=status.HTTP_400_BAD_REQUEST
            )
        circle.create_resource()
        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FileDetail(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def patch(self, request: Request, pk, fpk):
        """Update a file"""
        # TODO faire cette méthode
        try:
            resource = Resource.objects.get(id=id_resource)
            resource.tag()
        except Resource.DoesNotExist:
            raise Resource.DoesNotExist
        
        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)



    def get(self, request, *args, **kwargs):
        #TODO rajouter des méthodes pour serialiser file ou juste les envoyer dans un json
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
            resource = Resource.objects.get(id=id_resource)
            resource.tag()
        except Resource.DoesNotExist:
            raise Resource.DoesNotExist
        
        
        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResourceFolder(mixins.ListModelMixin, generics.GenericAPIView):
     queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    def post(self, request: Request, pk):
        """Create a new folder"""
        try:
            resource = Resource.objects.get(id=id_resource)
            # TODO create folder
        except Resource.DoesNotExist:
            raise Resource.DoesNotExist
        
        
        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request: Request, pk):
        """delete folder and file in folders"""
        try:
            resource = Resource.objects.get(id=id_resource)
            # TODO delete folder and file in folder
        except Resource.DoesNotExist:
            raise Resource.DoesNotExist
        
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
                status=status.HTTP_400_BAD_REQUEST
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
