from enum import unique
from functools import total_ordering
from typing import List

from enumfields import Enum

from .params import LTIParams


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

    TEACHING_STAFF_ROLES = [
        MENTOR,
        MANAGER,
        INSTRUCTOR,
        ADMINISTRATOR,
        CONTENT_DEVELOPER,
        TEACHING_ASSISTANT,
    ]

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
    def parse_from_lti(cls, params: LTIParams) -> 'Role':
        """
        Parses `params.roles` to find a valid LTI role name.

        Parameters
        ----------
        params : `LTIParams`
            LTI request parameters.
            
        Raises
        ------
        ValueError
            Raised if params.role does not correspond to a valid LTI role.
        """ 

        def parse(role: str) -> str:
            # role =
            # Learner |
            # urn:lti:role:ims/lis/Learner |
            # urn:lti:role:ims/lis/Learner/NonCreditLearner
            return role.replace('urn:lti:role:ims/lis/', '').split('/')[0]
        
        roles: List[str] = [
            parse(role) for role in params.roles.split(',')
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

        raise ValueError('Received unknown lti role: ' + params.roles)