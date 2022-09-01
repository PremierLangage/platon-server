import json
from asgiref.sync import async_to_sync

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from pl_loader.loader import Loader
from pl_sandbox.models import Sandbox

from pl_resources.models import Resource

from . import serializers

# Create your views here.
class LiveBuildView(APIView):

    def get(self, request: Request, *args, **kwargs):
        loader = Loader.get(request, kwargs.get('resource_id'))

        loader.parse()
        sandbox = Sandbox.objects.first()
        
        config = {
            "commands": [
                "python3 builder.py pl.json process.json"
            ],
            "result_path" : "process.json",
            "save": True
        }

        loader.build(sandbox, config)

        serializer = serializers.LiveAssetSerializer(loader)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, reqeust: Request, *args, **kwargs):
        return Response({'test': 'POST ok'})

class LiveView(APIView):

    def get(self, request: Request, *args, **kwargs):

        resource = Resource.objects.get(pk=kwargs.get('resource_id'))

        sandbox = Sandbox.objects.first()

        process = async_to_sync(sandbox.retrieve)(
            kwargs.get('env'),
            'process.json'
        )

        process_io = process.read()
        process.close()

        return Response({
            'env': kwargs.get('env'),
            'name': resource.name,
            'type': resource.type,
            'content': json.loads(process_io)
        })