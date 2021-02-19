from enum import unique
from functools import total_ordering

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
