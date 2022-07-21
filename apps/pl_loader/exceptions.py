from rest_framework import status
from rest_framework.exceptions import APIException

class LoaderError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Loader error.'
    default_code = 'loader_error'

class LoaderInitError(LoaderError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Loader init failed.'
    default_code = 'loader_unavailable'

class LoaderInitErrorUserNotAuthanticated(LoaderInitError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Not authanticated.'
    default_code = 'loader_unauthorized'

class LoaderInitErrorUserNotPermit(LoaderInitError):
    pass

class LoaderInitErrorResourceDoesNotExist(LoaderInitError):
    pass

class LoaderInitErrorResourceDirectoryDoesNotExist(LoaderInitError):
    pass

class LoaderParseError(LoaderError):
    pass

class LoaderStateError(LoaderError):
    pass