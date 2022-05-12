import os
from django.conf import settings
from pl_core.mixins import CrudViewSet
from pl_resources.files import Directory

from rest_framework import status
from rest_framework.response import Response

from .models import Loader
from .exceptions import LoaderException



# PUBLISHER

class Publisher(CrudViewSet):
    
    def get_loader(self, request, name, directory, version):
        path = 'main.pl'
        loader = Loader(name, directory, path, version)
        loader.load(request=request)
        return loader

    def env_publish(self, loader: Loader, request):
        sub_path = os.path.join(loader.name, 'tmp/content.tgz')
        export_path = os.path.join(settings.ASSETS_ROOT, sub_path)
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        loader.load_publish(request=request, export=export_path)
        

    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        name = kwargs.get('directory')
        version = query_params.get('version', 'master')
        try :
            directory = Directory.get(name, request.user)
            loader = self.get_loader(request, name, directory, version)
            self.env_publish(loader, request=request)
            return Response({
                "json" : loader.pl,
                "warnings" : loader.warning
            }, status=status.HTTP_200_OK)

        except FileNotFoundError as e:
            return Response({
                'error' : 'Bad request, resource not found'
            }, status = status.HTTP_400_BAD_REQUEST)

        except LoaderException as e:
            return Response({
                "error" : e.error
            }, status = e.status)

    def publish(self, request, *args, **kwargs):
        query_params = request.query_params
        name = kwargs.get('directory')
        version = query_params.get('version', 'master')
        try :
            directory = Directory.get(name, request.user)
            loader = self.get_loader(request, name, directory, version)
            loader.load_publish(request=request)
            return Response(status=status.HTTP_200_OK)

        except FileNotFoundError as e:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        except LoaderException as e:
            return Response(status = e.status)

    @classmethod
    def as_detail(cls):
        return cls.as_view({
            'get': 'get',
            'post': 'publish'
        })