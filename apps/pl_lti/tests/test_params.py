#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_params.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.test import TestCase
from pl_lti.params import LTIParams
from pl_lti.role import Role
from pl_lti.tests.mocks.params import UPEM_LMS_PARAMS


class LTIParamsTestCase(TestCase):

    def test_missing_mandatory(self):
        params = UPEM_LMS_PARAMS.clone()
        params.oauth_consumer_key = None
        with self.assertRaises(AssertionError):
            LTIParams.from_dict(params.to_dict())


    def test_from_dict_Ok(self):
        params = UPEM_LMS_PARAMS.clone()
        self.assertEqual(
            params,
            LTIParams.from_dict(params.to_dict())
        )
