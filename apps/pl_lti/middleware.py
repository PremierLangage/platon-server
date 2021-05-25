#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  middleware.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

import logging

from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

from pl_lti.utils import is_lti_request

from .params import LTIParams
from .signals import lti_request

logger = logging.getLogger(__name__)


class LTIAuthMiddleware(MiddlewareMixin):
    """
    Middleware for authenticating users via an LTI launch URL.
    If the request is an LTI launch request, then this middleware attempts to
    authenticate the username and signature passed in the POST data.
    If authentication is successful, the user is automatically logged in to
    persist the user in the session and LTI object will be added to request object.
    If the request is not an LTI launch request, do nothing.
    """


    def ensure_auth_middleware(self, request: HttpRequest):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):  # pragma: no cover
            logger.debug('improperly configured: request has no user attr')
            raise ImproperlyConfigured(
                "The Django LTI auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the LTIAuthMiddleware class.")


    def process_request(self, request: HttpRequest):
        self.ensure_auth_middleware(request)
        send_signal = False
        if is_lti_request(request):
            user = auth.authenticate(request=request)
            if user is not None:
                auth.login(request, user)
                params = LTIParams.from_dict(request.POST.dict())
                request.session['LTI'] = params.to_dict()
                send_signal = True
        setattr(request, 'LTI', request.session.get('LTI', {}))
        if send_signal:
            lti_request.send(sender=self.__class__, request=request)
