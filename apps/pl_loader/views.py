from rest_framework import permissions
from rest_framework.views import APIView
from pl_resources.models import Resource
from .loader import Loader
from django.http import HttpResponse
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class testParseView(APIView):
    
    def get(self, request, resource_id):
        loader = Loader.get(request, resource_id)
        loader.parse()
        return HttpResponse(json.dumps(loader.json["data"], indent=2, cls=SetEncoder))
    