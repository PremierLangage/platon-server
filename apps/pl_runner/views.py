from asgiref.sync import async_to_sync

from rest_framework.request import Request
from rest_framework.response import Response
from pl_resources.files import Directory
from pl_sandbox.models import Sandbox
from rest_framework.views import APIView

from django.http import JsonResponse

class Loader(APIView):

    def get(self, request: Request, *args, **kwargs):
        path = kwargs.get('path', '.')
        version = 'master'
        directory = kwargs.get('directory')
        directory = Directory.get(directory, request.user)

        config = {
            "commands" : [
                "echo 'Hello from sandbox'"
            ],
            "save": False
        }

        sandbox = Sandbox.objects.get(name="Default")
        request = async_to_sync(sandbox.execute)(request.user, config)

        return JsonResponse({'status' : 200})
        


        