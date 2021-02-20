#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_role.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from django.test import TestCase
from pl_lti.role import Role


class RoleTestCase(TestCase):

    def test_parse_role_lti_label(self):
        self.assertEqual(Role.LEARNER, Role.from_lti_role("Learner"))
        self.assertEqual(Role.ADMINISTRATOR, Role.from_lti_role("Administrator"))
        self.assertEqual(Role.LEARNER, Role.from_lti_role("Unknown"))



    def test_parse_role_lti_URN(self):
        self.assertEqual(Role.LEARNER, Role.from_lti_role("urn:lti:instrole:ims/lis/Learner"))
