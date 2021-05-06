import json
from typing import Optional

from django.contrib.auth.models import User

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




class CircleList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer

    def get(self, request, *args, **kwargs):
        """ok"""

        # TODO check user is logged 

        return self.list(request, *args, **kwargs)

    def post(self, request: Request):
        """ko"""

        # TODO check user is logged
        
        id_parent = request.data.get('parent_id')
        path = request.data.get('path')
        name = request.data.get('name')
        description = request.data.get('description')
        tags = request.data.get('tags')

        parent = None
        
        if id_parent is not None:
            parent = Circle.objects.get(id=id_parent)
        
        Circle = Circle.objects.create(
            parent=parent, name=name,
            description=description,
            tags=tags,
            path=path
        )
        
        if not Circle:
            return Response(
                RestError('Circle/not-found'),
                status=status.HTTP_404_NOT_FOUND
            )
        Circle.create_resource()
        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CircleDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """View that allow to retrieve the informations of a single Circle"""
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer

    def get(self, request: Request, pk):

        # TODO check user is logged

        return self.retrieve(request, pk=pk)


class CircleRegister(mixins.ListModelMixin, generics.GenericAPIView):
    """View that handle to register a user in a circle."""

    def post(self, request: Request, pk):
        
        # TODO update with auth
        user_id = request.data.get('user_id')


        try:
            user = User.objects.get(id=user_id)
            circle = Circle.objects.get(id=pk)
            circle.register(user)
        except Circle.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        except User.DoesNotExist:
            return Response(
                RestError('user/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        # TODO register

        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CircleKick(mixins.ListModelMixin, generics.GenericAPIView):
    """View that handle to kick a user from a circle."""

    def post(self, request: Request, pk):
        
         # TODO update with auth
        user_id = request.data.get('user_id')
        user_kicked = request.data.get('user_kicked')

        try:
            user_kicking = User.objects.get(id=user_id)
            user_kicked = User.objects.get(id=user_kicked)
            circle = Circle.objects.get(id=pk)
            circle.kick(user_kicking, user_kicked)
        except Circle.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        except User.DoesNotExist:
            return Response(
                RestError('user/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        # TODO register

        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)




class CirclePublish(mixins.ListModelMixin, generics.GenericAPIView):
    """View that handle to publish a user in a circle."""

    def post(self, request: Request, pk):
        
         # TODO update with auth
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            circle = Circle.objects.get(id=pk)
            circle.publish(user)
        except Circle.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        except User.DoesNotExist:
            return Response(
                RestError('user/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        # TODO register

        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CirclePraise(mixins.ListModelMixin, generics.GenericAPIView):
    """View that handle register a user in a circle."""

    def post(self, request: Request, pk):
        
         # TODO update with auth
        user_id = request.data.get('user_id')
        user_praised = request.data.get('user_praised')
        user_praised = request.data.get('praise')

        # TODO check fields

        try:
            user = User.objects.get(id=user_id)
            user_praised = User.objects.get(id=user_praised)
            circle = Circle.objects.get(id=pk)
            circle.praise(user, user_praised, praise)
        except Circle.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        except User.DoesNotExist:
            return Response(
                RestError('user/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 

        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CircleBlame(mixins.ListModelMixin, generics.GenericAPIView):
    """View that handle register a user in a circle."""
        
    def post(self, request: Request, pk):
        
         # TODO update with auth
        user_id = request.data.get('user_id')
        user_blamed = request.data.get('user_blamed')

        # TODO check fields

        try:
            user = User.objects.get(id=user_id)
            user_blamed = User.objects.get(id=user_blamed)
            circle = Circle.objects.get(id=pk)
            circle.blame(user, user_blamed)
        except Circle.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
        except User.DoesNotExist:
            return Response(
                RestError('user/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 

        serializer = CircleSerializer(circle)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CircleParents(mixins.ListModelMixin, generics.GenericAPIView):
    """View that handle register a user in a circle."""
    serializer_class = CircleSerializer
    queryset = Circle.objects.all()

    def get(self, request: Request, pk):

        # TODO check user is logged  
        tree_id = []
        tree_id.append(pk)

        try:
            circle = Circle.objects.get(id=pk)
            while(circle and circle.parent):
                circle = circle.parent
                tree_id.append(circle.id)
        except Circle.DoesNotExist:
            return Response(
                RestError('resource/not-found'),
                status=status.HTTP_404_NOT_FOUND
            ) 
                    
        queryset = queryset.filter(circle__pk__in=tree_id)
        return queryset


# ========== Resources ==============


class ResourcesList(mixins.ListModelMixin, generics.GenericAPIView):
    """Create more bail when we create models like exo, activity, ..."""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


    def post(self, request: Request, pk):
        # TODO check user is logged 
 
        # TODO create resource

        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        # TODO check user is logged
        return self.list(request, *args, **kwargs)


class ResourceDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView, generics.RetrieveUpdateDestroyAPIView):
    """View that allow to retrieve the informations of a single Resource."""
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    methods = ['get', 'patch']

    def get(self, request: Request, pk : int, pkr: int):

        # TODO check user is logged

        return self.retrieve(request, pk=pk, pkr=pkr)


# ========== Versions ==============

class VersionList(mixins.ListModelMixin, generics.GenericAPIView):
    """Create more bail when we create models like exo, activity, ..."""
    # TODO queryset = Resource.objects.all()
    # TODO serializer_class = ResourceSerializer


    def post(self, request: Request, pk):
        # TODO check user is logged 
 
        # TODO create resource

        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        # TODO check user is logged
        return self.list(request, *args, **kwargs)


class VersionDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView, generics.RetrieveUpdateDestroyAPIView):
    """View that allow to retrieve the informations of a single Resource."""
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    methods = ['get', 'patch']

    def get(self, request: Request, pk : int, pkr: int):

        # TODO check user is logged

        return self.retrieve(request, pk=pk, pkr=pkr)



# ==========  Files  ==============

class FileList(mixins.ListModelMixin, generics.GenericAPIView):
    """Create more bail when we create models like exo, activity, ..."""
    # TODO queryset = Resource.objects.all()
    # TODO serializer_class = ResourceSerializer


    def post(self, request: Request, pk):
        # TODO check user is logged 
 
        # TODO create resource

        serializer = ResourceSerializer(resource)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        # TODO check user is logged
        return self.list(request, *args, **kwargs)


class FileDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView, generics.RetrieveUpdateDestroyAPIView):
    """View that allow to retrieve the informations of a single Resource."""
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    methods = ['get', 'patch']

    def get(self, request: Request, pk : int, pkr: int):

        # TODO check user is logged

        return self.retrieve(request, pk=pk, pkr=pkr)


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
