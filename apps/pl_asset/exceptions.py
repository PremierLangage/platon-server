

class SandboxError(Exception):
    pass

class SandboxNotFoundError(Exception):
    """Raised when any sandbox are present."""
    pass

class SandboxDisabledError(SandboxError):
    """Raised when trying to launch a request to a disabled Sandbox."""
    pass
