class SandboxError(Exception):
    pass



class SandboxDisabledError(SandboxError):
    """Raised when trying to launch a request to a disabled Sandbox."""
    pass
