import asyncio

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import classonlymethod
from django.views.generic.base import View
from rest_framework import mixins, exceptions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class AsyncView(View):
    """Base Async View."""

    @classonlymethod
    def as_view(cls, **kwargs):
        """Set view returned by `View.as_view()` as a corountine."""
        view = super().as_view(**kwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine  # noqa
        return view


# https://stackoverflow.com/questions/30871033/django-rest-framework-remove-csrf
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CrudViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
):

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)

        # Override get_queryset to cache the result
        old_get_queryset = self.get_queryset

        def get_queryset():
            if not hasattr(self, '__get_queryset__'):
                self.__get_queryset__ = old_get_queryset()
            return self.__get_queryset__
        setattr(self, 'get_queryset', get_queryset)


        # Override get_object to cache the result
        old_get_object = self.get_object

        def get_object():
            try:
                if not hasattr(self, '__get_object__'):
                    self.__get_object__ = old_get_object()
                self.check_object_permissions(request, self.__get_object__)
                return self.__get_object__
            except ObjectDoesNotExist:
                raise exceptions.NotFound()
        setattr(self, 'get_object', get_object)

        return request

    def list(self, request, *args, **kwargs):
        if 'no_page' in self.request.query_params:
            self.pagination_class = None
        return super().list(request, *args, **kwargs)

    @classmethod
    def as_list(cls):
        return cls.as_view({'get': 'list', 'post': 'create'})

    @classmethod
    def as_detail(cls):
        return cls.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})
