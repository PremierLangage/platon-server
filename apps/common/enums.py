import enum



@enum.unique
class ErrorCode(enum.Enum):
    """Enum error code sent when a RESTful request fail."""
    JSONDecodeError = "INVALID_JSON"
    ValidationError = "INVALID_FIELD"
    DoesNotExist = "NOT_FOUND"
    PermissionDenied = "PERMISSION_DENIED"
    Http404 = "PAGE_NOT_FOUND"
    
    
    @classmethod
    def from_exception(cls, exc: Exception):
        return cls[exc.__class__.__name__]
