import asyncio
import functools

from django.views.decorators.http import require_http_methods



def require_http_methods_async(request_method_list):
    """Decorator to make a view only accept particular request methods.
    
    Usage:
    
    ```python
    @require_http_methods_async(["GET", "POST"])
    def my_view(request):
        # I can assume now that only GET or POST requests make it this far
        # ...
    ```
    
    Note that request methods should be in uppercase."""
    async def decorator(f):
        @functools.wraps(f)
        async def inner(*args, **kwargs):
            res = require_http_methods(request_method_list)(f)(*args, **kwargs)
            if asyncio.iscoroutine(res):
                return await res
            return res
        return inner
    
    return decorator


require_GET_async = require_http_methods(["GET"])
require_GET_async.__doc__ = "Decorator to require that a view only accepts the GET method."

require_HEAD_async = require_http_methods(["HEAD"])
require_HEAD_async.__doc__ = "Decorator to require that a view only accepts the PATCH method."

require_POST_async = require_http_methods(["POST"])
require_POST_async.__doc__ = "Decorator to require that a view only accepts the POST method."

require_DELETE_async = require_http_methods(["DELETE"])
require_DELETE_async.__doc__ = "Decorator to require that a view only accepts the DELETE method."

require_PUT_async = require_http_methods(["PUT"])
require_PUT_async.__doc__ = "Decorator to require that a view only accepts the PUT method."

require_PATCH_async = require_http_methods(["PATCH"])
require_PATCH_async.__doc__ = "Decorator to require that a view only accepts the PATCH method."
