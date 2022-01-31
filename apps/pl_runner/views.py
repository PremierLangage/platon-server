import os
from asgiref.sync import async_to_sync
from rest_framework.request import Request
from rest_framework.response import Response
from pl_resources.files import Directory
from pl_sandbox.models import Sandbox
from rest_framework.views import APIView
from pl_runner.parser import Parser
from pl_runner.utils import extends_dict

class Loader(APIView):

    def get(self, request: Request, *args, **kwargs):
        path = kwargs.get('path', '.')
        version = 'master'
        directory = kwargs.get('directory')
        directory = Directory.get(directory, request.user)

        parser = Parser(path, directory.read(path, version, request=request))
        loader, warnings = parser.parse()

        for extends in loader['__extends']:
            head, tail = os.path.split(extends)
            directory = Directory.get(head, request.user)
            file = directory.read(tail, version, request=request)
            following = Parser(tail, file)
            dic, new_warnings = following.parse()
            extends_dict(loader, dic)
            warnings = warnings + new_warnings

        config = {
            "commands" : [
                "python3 builder.py pl.json process.json 2> stderr.log",
                "echo 'Hello from sandbox'"
            ],
            "save" : False
        }

        sandbox = Sandbox.objects.get(name="Default")
        request = async_to_sync(sandbox.runner)(request.user, config, loader)

        return Response({"message" : "Wouaaa"})
        
        if path != '.':
            
            return Response(dic)
        else:
            return Response({"message" : "Not a valid file detected..."})
        return Response(directory.read(path, version, request=request))
        


        