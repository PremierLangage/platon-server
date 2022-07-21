import json
from asgiref.sync import async_to_sync

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from pl_sandbox.models import Sandbox

from .loader import Loader
from . import serializers

# Create your views here.
class LoaderView(APIView):

    def get(self, request: Request, *args, **kwargs):
        loader = Loader.get(request, kwargs.get('resource_id'))

        loader.parse()
        sandbox = Sandbox.objects.first()
        
        config = {
            "commands": [
                "python3 builder.py pl.json process.json"
            ],
            "result_path" : "process.json"
        }

        loader.build(sandbox, config)

        serializer = serializers.LiveAssetSerializer(loader)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, reqeust: Request, *args, **kwargs):
        return Response({'test': 'POST ok'})