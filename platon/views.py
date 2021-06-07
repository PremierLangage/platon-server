from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'auth-sign-in': reverse('pl_auth:sign-in', request=request, format=format),
        'auth-sign-out': reverse('pl_auth:sign-out', request=request, format=format),
        'auth-sign-refresh': reverse('pl_auth:refresh', request=request, format=format),
        'users': reverse('pl_users:user-list', request=request, format=format),
        'topics': reverse('pl_resources:topic-list', request=request, format=format),
        'levels': reverse('pl_resources:level-list', request=request, format=format),
        'circles': reverse('pl_resources:circle-list', request=request, format=format),
        'my-circle': reverse('pl_resources:circle-me', request=request, format=format),
        'circles-tree': reverse('pl_resources:circle-tree', request=request, format=format),
        'resources': reverse('pl_resources:resource-list', request=request, format=format),
        'recently-viewed-resources': reverse('pl_resources:resource-recent-views', request=request, format=format),
    })
