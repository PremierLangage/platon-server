import asyncio

from django.utils.decorators import classonlymethod
from django.views.generic.base import View



class AsyncView(View):
    """Base Async View."""
    
    @classonlymethod
    def as_view(cls, **kwargs):
        """Set view returned by `View.as_view()` as a corountine."""
        view = super().as_view(**kwargs)
        view._is_coroutine = asyncio.coroutines._is_coroutine  # noqa
        return view
