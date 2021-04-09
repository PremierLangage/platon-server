class RestError(dict):
    """ Representation of an error response from a request"""

    def __init__(self, code: str, detail=None):
        if detail is None:
            super().__init__(self, code=code)
        else:
            super().__init__(self, code=code, detail=detail)
