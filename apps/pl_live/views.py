import json, io, tarfile
from asgiref.sync import async_to_sync

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from pl_loader import utils
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
    
    def post(self, request: Request, *args, **kwargs):

        resource = Resource.objects.get(pk=kwargs.get('resource_id'))

        answer = json.loads(request.data.get('answer', {}))

        environment = io.BytesIO()
        with tarfile.open(fileobj=environment, mode="w:gz") as env:
            json_file = json.dumps(answer, indent=4)
            tar_file, tar_info = utils.string_to_tarfile('answer.json', json_file)
            env.addfile(fileobj=tar_file, tarinfo=tar_info)
        environment.seek(0)

        sandbox = Sandbox.objects.first()

        config = {
            "commands": [
                "ls -al > tmp.json"
            ],
            "environment": str(kwargs.get('env')),
            "result_path" : "tmp.json",
            "save": True
        }

        response = async_to_sync(sandbox.execute)(
            request.user,
            config,
            environment
        )

        environment.close()

        return Response({
            'env': response.response.environment,
            'name': resource.name,
            'type': resource.type,
            'answer': response.response.result
        })
    
# NEW

class LiveBuild(APIView):

    def post(self, request: Request, *args, **kwargs):
        loader = Loader.get(request, kwargs.get('id'))
        loader.parse()
        sandbox = Sandbox.objects.first()

        config = {
            "commands": [
                "python3 builder.py pl.json process.json"
            ],
            "save": True
        }

        loader.build(sandbox, config)
        return Response({
            "id": kwargs.get('id'),
            "env": str(loader.environment)
        }, status=status.HTTP_200_OK)
        

class LiveRetrieve(APIView):

    def get(self, request: Request, *args, **kwargs):
        resource = Resource.objects.get(pk=kwargs.get('id'))
        sandbox = Sandbox.objects.first()

        try:
            process = async_to_sync(sandbox.retrieve)(
                kwargs.get('env'),
                kwargs.get('path')
            )
            output = json.loads(process.read())
            process.close()
        except:
            output = {}

        return Response({
            "id": kwargs.get('id'),
            "env": kwargs.get('env'),
            "name": resource.name,
            "type": resource.type,
            "content": output
        })

class LiveGrade(APIView):

    def _serialize_answer(self, answer : dict) -> dict:
        res = {}

        def aux(dic :dict):
            print(dic)
            if isinstance(dic, dict):
                if all(map(str.isnumeric,dic.keys())) and list(sorted(map(int, dic.keys()))) == list(range(len(dic))):
                    return [dic[str(i)] for i in range(len(dic))]
                else:
                    return {k: aux(v) for k, v in dic.items()}
            else:
                return dic

        for key, value in answer.items():
            if isinstance(value, dict):
                res[key] = aux(value)
            else:
                res[key] = value
        return res

    def post(self, request: Request, *args, **kwargs):
        resource = Resource.objects.get(pk=kwargs.get('id'))
        answer = self._serialize_answer(request.data.get('answers', {}))
        environment = io.BytesIO()

        with tarfile.open(fileobj=environment, mode="w:gz") as env:
            json_file = json.dumps(answer, indent=4)
            tar_file, tar_info = utils.string_to_tarfile('answers.json', json_file)
            env.addfile(fileobj=tar_file, tarinfo=tar_info)
        environment.seek(0)
        config = {
            "commands": [
                "cat process.json > processed.json",
                "python3 grader.py pl.json answers.json processed.json feedback.html"
            ],
            "environment": str(kwargs.get('env')),
            "save": True
        }
        sandbox = Sandbox.objects.first()
        req = async_to_sync(sandbox.execute)(
            request.user,
            config,
            environment
        )
        environment.close()
        return Response({
            "id": kwargs.get('id'),
            "env": req.response.environment
        }, status=status.HTTP_200_OK)
