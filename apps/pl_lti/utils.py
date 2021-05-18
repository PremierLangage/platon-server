#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

import logging
from typing import Tuple
from django.http.request import HttpRequest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.utils import IntegrityError

from pl_lti.models import LMS, LTIUser
from pl_lti.params import LTIParams
from pl_lti.validator import is_valid_request

logger = logging.getLogger(__name__)


def find_lms(params: LTIParams) -> LMS:
    """Find a LMS registered with `params.tool_consumer_instance_guid` as a `guid` value.

    Args:
        params (LTIParams): A LTI request parameters.

    Raises:
        PermissionDenied

    Returns:
        LMS: The retrieved LMS object.
    """

    guid = params.tool_consumer_instance_guid
    oauth_consumer_key = params.oauth_consumer_key

    if not guid:
        logger.error("LTI: Request doesn't contain an tool_consumer_instance_guid; can't continue.")
        raise PermissionDenied("LTI: Request doesn't contain an tool_consumer_instance_guid; can't continue.")

    if not oauth_consumer_key:
        logger.error("LTI: Request doesn't contain an oauth_consumer_key; can't continue.")
        raise PermissionDenied("LTI: Request doesn't contain an oauth_consumer_key; can't continue.")

    try:
        lms = LMS.objects.get(guid=guid)
        if lms.client_id != oauth_consumer_key:
            logger.error(f"LTI: There is no LMS registered with the key {oauth_consumer_key}")
            raise PermissionDenied(f"LTI: There is no LMS registered with the key {oauth_consumer_key}")
        return lms
    except ObjectDoesNotExist:
        logger.error(f"LTI: There is no LMS registered with the guid {guid}")
        raise PermissionDenied(f"LTI: There is no LMS registered with the guid {guid}")


def create_lti_user(lms: LMS, params: LTIParams) -> User:
    """Creates a `LTIUser` object from a LTI request params.

    If the user already exists then it's informations will be updated

    Args:
        lms (LMS): LMS on which the user belongs to.
        params (LTIParams): The LTI request parameters.

    Returns:
        User: Django user model object.
    """

    user_id = params.user_id
    email = params.lis_person_contact_email_primary
    last_name = params.lis_person_name_family
    first_name = params.lis_person_name_given

    username = (first_name[0].lower() + last_name.lower())

    try:
        lti = LTIUser.objects.get(lms=lms, lms_user_id=user_id)
        logger.info(f'LTI: Found an existing user for {username}')
    except ObjectDoesNotExist:
        logger.info(f'LTI: Creating a new user for {username}')
        i = 0
        UserModel = get_user_model()
        while True:
            try:
                user = UserModel.objects.create_user(
                    username=username + ("" if not i else str(i))
                )
            except IntegrityError:
                i += 1
                continue
            break
        lti = LTIUser.objects.create(
            lms=lms,
            user=user,
            lms_user_id=user_id
        )

    lti.user.email = email
    lti.user.last_name = last_name
    lti.user.first_name = first_name
    lti.user.save()

    return lti.user


def parse_lti_request(request) -> Tuple[LMS, LTIParams]:
    """Try to parses the given request as an LTI request.

    Args:
        request ([type]): [description]

    Raises:
        PermissionDenied: If the request is invalid.

    Returns:
        [tuple]: An (lms, params) tuple where lms is the lms
        where the request coming from and params the parameters of the request.
    """

    params = LTIParams.from_dict(request.POST.dict())
    if not params.user_id:
        logger.error("LTI: Missing argument user_if not params.user_id")
        raise PermissionDenied("LTI: Missing argument user_if not params.user_id")
    if not params.lis_person_name_given:
        logger.error("LTI: Missing argument lis_person_name_given")
        raise PermissionDenied("LTI: Missing argument lis_person_name_given")
    if not params.lis_person_name_family:
        logger.error("LTI: Missing argument lis_person_name_family")
        raise PermissionDenied("LTI: Missing argument lis_person_name_family")
    if not params.lis_person_contact_email_primary:
        logger.error("LTI: Missing argument lis_person_contact_email_primary")
        raise PermissionDenied("LTI: Missing argument lis_person_contact_email_primary")

    lms = find_lms(params)

    # TODO
    request_is_valid = is_valid_request(lms.client_id, lms.client_secret, request)
    # if not request_is_valid:
    #    logger.error("LTI: Oauth signature check failed.")
    #    raise PermissionDenied("LTI: Oauth signature check failed.")

    return lms, params


def is_lti_request(request: HttpRequest):
    if request.method != 'POST':
        return False
    return request.POST.get('lti_message_type') == 'basic-lti-launch-request'
