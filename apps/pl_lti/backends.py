#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  params.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

import logging

from django.contrib.auth.backends import ModelBackend

from pl_lti.utils import create_lti_user, is_lti_request, parse_lti_request

logger = logging.getLogger(__name__)


class LTIAuthBackend(ModelBackend):
    """
    Creates a User object from a LTI request if needed and set the user
    as the new logged one.
    """


    def authenticate(self, request, username=None, password=None, **kwargs):
        if is_lti_request(request):
            logger.info("LTI: Authenticating request...")
            try:
                user = create_lti_user(
                    *parse_lti_request(request)
                )
                logger.info(f"LTI: Succesfully authenticated {user.username}.")
                return user
            except:
                logger.error("LTI: Authentication failed.")
