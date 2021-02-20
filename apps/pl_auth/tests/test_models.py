#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_models.py
#
#

from django.contrib.auth.models import User
from django.test import TestCase
from pl_lti.role import Role


class ModelsTestCase(TestCase):
    """ Test functions of pl_auth.models modules. """


    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user', password='12345', id=100)


    def test_profile_str(self):
        self.assertEqual(str(self.user.profile), "user's Profile")


    def test_is_admin(self):
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.profile.role = Role.LEARNER
        self.assertFalse(self.user.profile.is_admin())

        self.user.profile.role = Role.ADMINISTRATOR
        self.assertTrue(self.user.profile.is_admin())

        self.user.profile.role = Role.LEARNER
        self.user.is_superuser = True
        self.assertTrue(self.user.profile.is_admin())

        self.user.is_superuser = False
        self.user.is_staff = True
        self.assertTrue(self.user.profile.is_admin())
