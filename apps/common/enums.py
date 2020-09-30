import enum



class ErrorCode(enum.Enum):
    """Enum error code sent when a RESTful request fail."""
    JSONDecodeError = "INVALID_JSON"
    ValidationError = "INVALID_FIELD"
    DoesNotExist = "NOT_FOUND"
    PermissionDenied = "PERMISSION_DENIED"
    Http404 = "PAGE_NOT_FOUND"
    UNKNOWN = "UNKNOWN"
    
    
    @classmethod
    def from_exception(cls, exc: Exception):
        """Return the `ErrorCode` corresponding to an Exception."""
        try:
            return cls[exc.__class__.__name__]
        except KeyError:
            return cls.UNKNOWN
