#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  role.py
#
#  Authors:
#       - Mamadou CISSE <mciissee.@gmail.com>
#

from enum import unique
from functools import total_ordering
from typing import List

from enumfields import Enum


@unique
@total_ordering
class Role(Enum):
    """Used by .models.Profile to define the user's role."""

    LEARNER = 0
    INSTRUCTOR = 1
    CONTENT_DEVELOPER = 2
    MEMBER = 3
    MANAGER = 4
    MENTOR = 5
    ADMINISTRATOR = 6
    TEACHING_ASSISTANT = 7

    class Label:
        LEARNER = 'Learner'
        INSTRUCTOR = 'Instructor'
        CONTENT_DEVELOPER = 'ContentDeveloper'
        MEMBER = 'Member'
        MANAGER = 'Manager'
        MENTOR = 'Mentor'
        ADMINISTRATOR = 'Administrator'
        TEACHING_ASSISTANT = 'TeachingAssistant'


    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented  # pragma: no cover


    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented  # pragma: no cover


    @classmethod
    def from_lti_role(cls, roles: str) -> 'Role':
        """
        Extract a valid Role from `roles`

        Parameters
        ----------
        roles : `str`
            A comma separated list of roles as specified in the LTI specifications.

        Returns
        -------
        role: `Role`
        The parsed role or `Role.LEARNER`
        """

        def parse(role: str) -> str:
            # role =
            # Learner |
            # urn:lti:role:ims/lis/Learner |
            # urn:lti:role:ims/lis/Learner/NonCreditLearner
            return (
                role.replace("urn:lti:instrole:ims/lis/", "")
                    .replace("urn:lti:sysrole:ims/lis/", "")
                    .replace("urn:lti:role:ims/lis/", "")
                    .strip()
            ).split('/')[0]

        roles: List[str] = [
            parse(r) for r in roles.split(',')
        ]

        role_map = {
            'Learner': Role.LEARNER,
            'Instructor': Role.INSTRUCTOR,
            'ContentDeveloper': Role.CONTENT_DEVELOPER,
            'Member': Role.MEMBER,
            'Manager': Role.MANAGER,
            'Mentor': Role.MENTOR,
            'Administrator': Role.ADMINISTRATOR,
            'TeachingAssistant': Role.TEACHING_ASSISTANT,
        }

        for name, role in role_map.items():
            if name in roles:
                return role
        return Role.LEARNER


TEACHING_STAFF_ROLES = [
    Role.MENTOR,
    Role.MANAGER,
    Role.INSTRUCTOR,
    Role.ADMINISTRATOR,
    Role.CONTENT_DEVELOPER,
    Role.TEACHING_ASSISTANT,
]
