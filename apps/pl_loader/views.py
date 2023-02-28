from pl_resources.models import Resource
from .loader import Loader
from django.http import HttpResponse
import json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def testParseView(request, resource_id):
    loader = Loader.get(request, resource_id)
    loader.parse()
    return HttpResponse(json.dumps(loader.json, indent=2, cls=SetEncoder))