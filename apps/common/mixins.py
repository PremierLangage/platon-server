import asyncio

from django.utils.decorators import classonlymethod
from django.views.generic.base import View
from rest_framework.authentication import SessionAuthentication


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
