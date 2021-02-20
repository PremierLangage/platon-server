#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_utils.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from mock import patch
from logging import Logger

from pl_lti.models import LMS
from pl_lti.utils import find_lms

from .mocks.params import UPEM_LMS_PARAMS



class LTIMiddlewareCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.lms = LMS.objects.create(
            guid=UPEM_LMS_PARAMS.tool_consumer_instance_guid,
            name=UPEM_LMS_PARAMS.tool_consumer_instance_name,
            url=UPEM_LMS_PARAMS.tool_consumer_instance_url,
            outcome_url=UPEM_LMS_PARAMS.lis_outcome_service_url,
            client_id=UPEM_LMS_PARAMS.oauth_consumer_key,
            client_secret="client_secret"
        )


    @patch('pl_lti.utils.logger')
    def test_find_lms_no_consumer_key(self, logger: Logger):
        params = UPEM_LMS_PARAMS.clone()
        params.oauth_consumer_key = ""
        with self.assertRaises(PermissionDenied):
            find_lms(params)
        self.assertIn("oauth_consumer_key", str(logger.error.call_args[0][0]))


    @patch('pl_lti.utils.logger')
    def test_find_lms_no_consumer_guid(self, logger: Logger):
        params = UPEM_LMS_PARAMS.clone()
        params.tool_consumer_instance_guid = ""
        with self.assertRaises(PermissionDenied):
            find_lms(params)
        self.assertIn("tool_consumer_instance_guid", str(logger.error.call_args[0][0]))


    @patch('pl_lti.utils.logger')
    def test_find_lms_wrong_consumer_key(self, logger: Logger):
        params = UPEM_LMS_PARAMS.clone()
        params.oauth_consumer_key = "SD"
        with self.assertRaises(PermissionDenied):
            find_lms(params)
        self.assertIn(params.oauth_consumer_key, str(logger.error.call_args[0][0]))


    @patch('pl_lti.utils.logger')
    def test_find_lms_wrong_consumer_guid(self, logger: Logger):
        params = UPEM_LMS_PARAMS.clone()
        params.tool_consumer_instance_guid = "DSD"
        with self.assertRaises(PermissionDenied):
            find_lms(params)
        self.assertIn(params.tool_consumer_instance_guid, str(logger.error.call_args[0][0]))


    @patch('pl_lti.utils.logger')
    def test_find_lms_success(self, logger: Logger):
        params = UPEM_LMS_PARAMS.clone()
        lms = find_lms(params)
        self.assertEqual(lms, self.lms)

    # TODO test create_lti_user
    # TODO test parse_lti_request
    # TODO test is_lti_request
