import json
from typing import Optional

import dgeq
from channels.db import database_sync_to_async
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import Http404, JsonResponse

from pl_core.async_db import has_perm_async
from pl_core.enums import ErrorCode
from pl_core.mixins import AsyncView
from pl_core.validators import check_unknown_fields, check_unknown_missing_fields
from .models import CommandResult, ContainerSpecs, Request, Response, Sandbox, SandboxSpecs, Usage



class SandboxView(AsyncView):
    """Contains views used for CRUD on the `Sandbox` model."""
    
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    
    
    async def get(self, request, pk: Optional[int] = None):
        """Allow to get a single or a collection of `Sandbox`."""
        try:
            if not await has_perm_async(request.user, "pl_sandbox.view_sandbox"):
                raise PermissionDenied("Missing view permission on Sandbox")
            
            if pk is not None:
                sandbox = await database_sync_to_async(Sandbox.objects.get)(pk=pk)
                response = {
                    "status": True,
                    "row":    await database_sync_to_async(dgeq.serialize)(sandbox)
                }
            else:
                query = dgeq.GenericQuery(
                    Sandbox, request.GET, user=request.user, use_permissions=True
                )
                response = await database_sync_to_async(query.evaluate)()
            status = 200
        
        except Sandbox.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        return JsonResponse(response, status=status)
    
    
    async def post(self, request, pk: Optional[int] = None):
        """Allow to create a new `Sandbox`."""
        try:
            if pk is not None:
                raise Http404("Page not found")
            
            if not await has_perm_async(request.user, "pl_sandbox.create_sandbox"):
                raise PermissionDenied("Missing create permission on Sandbox")
            
            kwargs = json.loads(request.body)
            check_unknown_missing_fields({"name", "url", "enabled"}, kwargs)
            sandbox = Sandbox(**kwargs)
            await database_sync_to_async(sandbox.full_clean)()
            await database_sync_to_async(sandbox.save)()
            response = {
                "status": True,
                "row":    await database_sync_to_async(dgeq.serialize)(sandbox)
            }
            status = 201
        
        except json.JSONDecodeError as e:  # pragma
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 400
        
        except ValidationError as e:
            response = {
                "status":  False,
                "message": str(e.message_dict),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 400
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        except Http404 as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        return JsonResponse(response, status=status)
    
    
    async def delete(self, request, pk: Optional[int] = None):
        """Allow to delete a `Sandbox`"""
        try:
            if pk is None:
                raise Http404("Page not found")
            if not await has_perm_async(request.user, "pl_sandbox.delete_sandbox"):
                raise PermissionDenied("Missing delete permission on Sandbox")
            
            sandbox = await database_sync_to_async(Sandbox.objects.get)(pk=pk)
            response = {
                "status": True,
                "row":    await database_sync_to_async(dgeq.serialize)(sandbox)
            }
            await database_sync_to_async(sandbox.delete)()
            status = 200
        
        except Sandbox.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        except Http404 as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        return JsonResponse(response, status=status)
    
    
    async def patch(self, request, pk: Optional[int] = None):
        """Allow to modify a `Sandbox`."""
        try:
            if pk is None:
                raise Http404("Page not found")
            
            if not await has_perm_async(request.user, "pl_sandbox.change_sandbox"):
                raise PermissionDenied("Missing change permission on Sandbox")
            
            sandbox = await database_sync_to_async(Sandbox.objects.get)(pk=pk)
            kwargs = json.loads(request.body)
            check_unknown_fields({"name", "url", "enabled"}, kwargs)
            for k, v in kwargs.items():
                setattr(sandbox, k, v)
            await database_sync_to_async(sandbox.full_clean)()
            await database_sync_to_async(sandbox.save)()
            
            response = {
                "status": True,
                "row":    await database_sync_to_async(dgeq.serialize)(sandbox)
            }
            status = 200
        
        except Sandbox.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except json.JSONDecodeError as e:  # pragma
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 400
        
        except ValidationError as e:
            response = {
                "status":  False,
                "message": str(e.message_dict),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 400
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        except Http404 as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        return JsonResponse(response, status=status)
    
    
    async def put(self, request, pk: Optional[int] = None):
        """Allow to overwrite a `Sandbox`."""
        try:
            if pk is None:
                raise Http404("Page not found")
            
            if not await has_perm_async(request.user, "pl_sandbox.change_sandbox"):
                raise PermissionDenied("Missing change permission on Sandbox")
            
            # Check that the sandbox exists
            await database_sync_to_async(Sandbox.objects.get)(pk=pk)
            
            kwargs = json.loads(request.body)
            check_unknown_missing_fields({"name", "url", "enabled"}, kwargs)
            sandbox = await database_sync_to_async(Sandbox.objects.get)(pk=pk)
            for k, v in kwargs.items():
                setattr(sandbox, k, v)
            await database_sync_to_async(sandbox.full_clean)()
            await database_sync_to_async(sandbox.save)()
            
            response = {
                "status": True,
                "row":    await database_sync_to_async(dgeq.serialize)(sandbox)
            }
            status = 200
        
        except Sandbox.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except json.JSONDecodeError as e:  # pragma
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 400
        
        except ValidationError as e:
            response = {
                "status":  False,
                "message": str(e.message_dict),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 400
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        except Http404 as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        return JsonResponse(response, status=status)



class SandboxSpecsView(AsyncView):
    """Allow to get a single or a collection of `SandboxSpecs`."""
    
    http_method_names = ['get']
    
    
    async def get(self, request, pk: Optional[int] = None):
        try:
            if not await has_perm_async(request.user, "pl_sandbox.view_sandboxspecs"):
                raise PermissionDenied("Missing view permission on SandboxSpecs")
            
            if pk is not None:
                specs = await database_sync_to_async(SandboxSpecs.objects.get)(pk=pk)
                response = {
                    "status": True,
                    "row":    await database_sync_to_async(dgeq.serialize)(specs)
                }
            else:
                query = dgeq.GenericQuery(
                    SandboxSpecs, request.GET, user=request.user, use_permissions=True
                )
                response = await database_sync_to_async(query.evaluate)()
            status = 200
        
        except SandboxSpecs.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        return JsonResponse(response, status=status)



class ContainerSpecsView(AsyncView):
    """Allow to get a single or a collection of `ContainerSpecs`."""
    
    http_method_names = ['get']
    
    
    async def get(self, request, pk: Optional[int] = None):
        try:
            if not await has_perm_async(request.user, "pl_sandbox.view_containerspecs"):
                raise PermissionDenied("Missing view permission on ContainerSpecs")
            
            if pk is not None:
                specs = await database_sync_to_async(ContainerSpecs.objects.get)(pk=pk)
                response = {
                    "status": True,
                    "row":    await database_sync_to_async(dgeq.serialize)(specs)
                }
            else:
                query = dgeq.GenericQuery(
                    ContainerSpecs, request.GET, user=request.user, use_permissions=True
                )
                response = await database_sync_to_async(query.evaluate)()
            status = 200
        
        except ContainerSpecs.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        return JsonResponse(response, status=status)



class UsageView(AsyncView):
    """Allow to get a single or a collection of `Usage`."""
    
    http_method_names = ['get']
    
    
    async def get(self, request, pk: Optional[int] = None):
        try:
            if not await has_perm_async(request.user, "pl_sandbox.view_usage"):
                raise PermissionDenied("Missing view permission on Usage")
            
            if pk is not None:
                usage = await database_sync_to_async(Usage.objects.get)(pk=pk)
                response = {
                    "status": True,
                    "row":    await database_sync_to_async(dgeq.serialize)(usage)
                }
            else:
                query = dgeq.GenericQuery(
                    Usage, request.GET, user=request.user, use_permissions=True
                )
                response = await database_sync_to_async(query.evaluate)()
            status = 200
        
        except Usage.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        return JsonResponse(response, status=status)



class ResponseView(AsyncView):
    """Allow to get a single or a collection of `Response`."""
    
    http_method_names = ['get']
    
    
    async def get(self, request, pk: Optional[int] = None):
        try:
            if not await has_perm_async(request.user, "pl_sandbox.view_response"):
                raise PermissionDenied("Missing view permission on Response")
            
            if pk is not None:
                execution = await database_sync_to_async(Response.objects.get)(pk=pk)
                response = {
                    "status": True,
                    "row":    await database_sync_to_async(dgeq.serialize)(execution)
                }
            else:
                query = dgeq.GenericQuery(
                    Response, request.GET, user=request.user, use_permissions=True
                )
                response = await database_sync_to_async(query.evaluate)()
            status = 200
        
        except Response.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        return JsonResponse(response, status=status)



class CommandResultView(AsyncView):
    """Allow to get a single or a collection of `CommandResult`."""
    
    http_method_names = ['get']
    
    
    async def get(self, request, pk: Optional[int] = None):
        try:
            if not await has_perm_async(request.user, "pl_sandbox.view_commandresult"):
                raise PermissionDenied("Missing view permission on CommandResult")
            
            if pk is not None:
                execution = await database_sync_to_async(CommandResult.objects.get)(pk=pk)
                response = {
                    "status": True,
                    "row":    await database_sync_to_async(dgeq.serialize)(execution)
                }
            else:
                query = dgeq.GenericQuery(
                    CommandResult, request.GET, user=request.user, use_permissions=True
                )
                response = await database_sync_to_async(query.evaluate)()
            status = 200
        
        except CommandResult.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        return JsonResponse(response, status=status)



class RequestView(AsyncView):
    """Allow to get a single or a collection of `Request`."""
    
    http_method_names = ['get']
    
    
    async def get(self, request, pk: Optional[int] = None):
        try:
            if not await has_perm_async(request.user, "pl_sandbox.view_request"):
                raise PermissionDenied("Missing view permission on Request")
            
            if pk is not None:
                execution = await database_sync_to_async(Request.objects.get)(pk=pk)
                response = {
                    "status": True,
                    "row":    await database_sync_to_async(dgeq.serialize)(execution)
                }
            else:
                query = dgeq.GenericQuery(
                    Request, request.GET, user=request.user, use_permissions=True
                )
                response = await database_sync_to_async(query.evaluate)()
            status = 200
        
        except Request.DoesNotExist as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 404
        
        except PermissionDenied as e:
            response = {
                "status":  False,
                "message": str(e),
                "code":    ErrorCode.from_exception(e).value
            }
            status = 403
        
        return JsonResponse(response, status=status)
