from django.contrib.auth.models import User
from rest_framework import generics, mixins

from .serializers import UserSerializer


class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    """View that allow to retrieve the informations of all the registerd users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UserDetailView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """View that allow to retrieve the informations of a single user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
