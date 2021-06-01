from django.contrib.auth import get_user_model
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from pl_users.filters import UserFilter

from .serializers import UserSerializer

User = get_user_model()


class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
    """View that allow to retrieve the informations of all the registerd users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['username', 'last_name', 'first_name', 'email']
    filter_class = UserFilter

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
