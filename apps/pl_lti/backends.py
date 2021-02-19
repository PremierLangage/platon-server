import logging
import sys

import oauth2
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import IntegrityError

from .models import LMS, LTIUser
from .params import LTIParams
from .validator import is_valid_request

logger = logging.getLogger(__name__)



class LTIAuthBackend(ModelBackend):
    """
    By default, the ``authenticate`` method creates ``User`` objects for
    usernames that don't already exist in the database.  Subclasses can disable
    this behavior by setting the ``create_unknown_user`` attribute to
    ``False``.
    """


    def authenticate(self, request, username=None, password=None, **kwargs):
        logger.info("Starting LTI authentication process")

        logout(request)

        params = LTIParams.from_dict(request.POST.dict())
        lms = self.find_lms(params)

        try:
            request_is_valid = True
            if 'test' not in sys.argv:
                request_is_valid = is_valid_request(lms.client_id, lms.client_secret, request)
        except oauth2.Error:
            request_is_valid = False

        if not request_is_valid:
            logger.error("LTIAuth: Invalid request: signature check failed.")
            raise PermissionDenied("LTIAuth: Invalid request: signature check failed.")

        if not params.user_id:
            logger.error("LTIAuth: Missing argument user_if not params.user_id")
            raise PermissionDenied("LTIAuth: Missing argument user_if not params.user_id")

        if not params.lis_person_name_given:
            logger.error("LTIAuth: Missing argument lis_person_name_given")
            raise PermissionDenied("LTIAuth: Missing argument lis_person_name_given")

        if not params.lis_person_name_family:
            logger.error("LTIAuth: Missing argument lis_person_name_family")
            raise PermissionDenied("LTIAuth: Missing argument lis_person_name_family")

        if not params.lis_person_contact_email_primary:
            logger.error("LTIAuth: Missing argument lis_person_contact_email_primary")
            raise PermissionDenied("LTIAuth: Missing argument lis_person_contact_email_primary")

        uid = params.user_id
        email = params.lis_person_contact_email_primary
        last_name = params.lis_person_name_family
        first_name = params.lis_person_name_given

        username = (first_name[0].lower() + last_name.lower())

        lti = self.find_lti_user(username, lms, uid)

        if email:
            lti.user.email = email
        if first_name:
            lti.user.first_name = first_name
        if last_name:
            lti.user.last_name = last_name

        lti.user.save()

        logger.info(f"LTIAuth: User '{username}' has been authenticated")
        return lti.user


    def find_lms(self, params: LTIParams) -> LMS:
        guid = params.tool_consumer_instance_guid
        if guid is None:
            logger.error("LTIAuth: Request doesn't contain an tool_consumer_instance_guid; can't continue.")
            raise PermissionDenied("LTIAuth: Request doesn't contain an tool_consumer_instance_guid; can't continue.")
        try:
            return LMS.objects.get(
                guid=guid,
            )
        except ObjectDoesNotExist:
            logger.error(f"LTIAuth: There is no LMS registered with the guid {guid}")
            raise PermissionDenied(f"LTIAuth: There is no LMS registered with the guid {guid}")


    def find_lti_user(self, username: str, lms: LMS, uid: int) -> LTIUser:
        try:
            logger.info('LTIAuth: found an existing user for %s' % username)
            lti = LTIUser.objects.get(lms_user_id=uid, lms=lms)
        except ObjectDoesNotExist:
            logger.info('LTIAuth: created a new user for %s' % username)
            i = 0
            UserModel = get_user_model()
            while True:
                try:
                    user = UserModel.objects.create_user(
                        username=username + ("" if not i else str(i)))
                except IntegrityError:
                    i += 1
                    continue
                break
            lti = LTIUser.objects.create(user=user, lms=lms, lms_user_id=uid)
        return lti
