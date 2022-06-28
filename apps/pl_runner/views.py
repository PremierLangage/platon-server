import json
from asgiref.sync import async_to_sync

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from . import serializers, models

from pl_core.mixins import CrudViewSet
from pl_loader.models import Loader
from pl_sandbox.models import Sandbox, Request

# Create your views here.
class RunnerViewSet(CrudViewSet):
    
    lookup_field = 'pk'

    permission_classes = (AllowAny,)
    serializer_class = serializers.RunnerSerializer

    def get_queryset(self):
        return models.Runner.objects.all()
    
    def get_view(self, request, *args, **kwargs):
        if 'asset' not in kwargs:
            return Response({
                'detail': 'Invalid asset'
            }, status.HTTP_404_NOT_FOUND)
        asset = kwargs.get('asset')
        asset = models.Asset.objects.filter(id=asset)
        asset = asset[0]
        
        runner = models.Runner.build(request, asset)
        if runner.is_builded:
            return Response(runner.render(), status.HTTP_200_OK)

        return Response({
            'detail' : 'Unexpected error'
        }, status.HTTP_404_NOT_FOUND)

    def eval(self, request, *args, **kwargs):   
        asset = kwargs.get('asset')
        asset = models.Asset.objects.get(id=asset)
        if not asset:
            return Response("Asset id Invalid", status.HTTP_404_NOT_FOUND)
        runner = models.Runner.eval(request, asset)
        if runner.evaluated:
            print("DEBUG", runner.evaluated)
            eval_json = json.loads(runner.evaluated.response.result)
            return Response(eval_json, status.HTTP_200_OK)

        return Response({
            'detail' : 'Unexpected error'
        }, status.HTTP_404_NOT_FOUND)
    
        
    def get_live(self, request, *args, **kwargs):
        query_params = request.query_params
        directory = kwargs.get('directory')
        version = query_params.get('version', 'master')

        loader = Loader.get_loader(request, directory, version)
        environment = loader.get_env(request, version)

        sandbox = Sandbox.objects.first()

        config = {
            "commands": [
                "python3 builder.py pl.json process.json"
            ],
            "result_path" : "process.json"
        }

        request: Request = async_to_sync(sandbox.execute)(
            request.user,
            config,
            environment
        )

        if environment is not None:
            environment.close()

        return Response(json.loads(request.response.result), status.HTTP_200_OK)

    @classmethod
    def as_runner(cls):
        return cls.as_view({
            'get' : 'get_view',
            'post' : 'eval'
        })

    @classmethod
    def as_live(cls):
        return cls.as_view({
            'get' : 'get_live'
        })
    