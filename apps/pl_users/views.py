from django.contrib.auth.models import User
from pl_core.errors import RestError
from rest_framework import generics, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    """View that allow to retrieve the informations of all the registerd users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    View that allow to retrieve the informations of a single user.
    If provided 'pk' is "me" then return the current user.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        if kwargs.get(self.lookup_field) == 'me':
            return Response(self.get_serializer(request.user).data)
        return self.retrieve(request, *args, **kwargs)
