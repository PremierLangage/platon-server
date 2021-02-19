from django.contrib.auth.models import User
from django.db import models


class LMS(models.Model):
    """LMS model"""

    guid: str = models.CharField(max_length=200, blank=True)
    """GUID of the LMS corresponding to the
    tool_consumer_instance_guid parameter of the LTI request.
    Most of the time, it is the DNS of the LMS.
    For example:
    elearning.u-pem.fr.
    """

    name: str = models.CharField(max_length=200)
    """Name that identifies the LMS, for example: Moodle UPEM."""

    url: str = models.CharField(max_length=200)
    """URL of the LMS, for example: https://elearning.u-pem.fr/"""

    outcome_url: str = models.URLField(max_length=200)
    """URL on which to post back results to a LMS.
    Correspond to the lis_outcome_service_url
    param of a LTI request
    """

    client_id: str = models.CharField(max_length=200)
    """Key that you'll need to enter on the LMS
    when creating a LTI activity.
    """

    client_secret: str = models.CharField(max_length=200)
    """Secret that you'll need to enter on the LMS
    when creating a LTI activity.
    """


    class Meta:
        verbose_name = 'lms'
        verbose_name_plural = 'lms'


    def __str__(self) -> str:
        return self.name


class LTIUser(models.Model):
    """LTIUser acts as the link between an user on a LMS
    and an user on PLaTon.
    """

    user: User = models.ForeignKey(User, related_name="lti_users", on_delete=models.CASCADE)
    """Reference to the PLaTon user related to this LTI user. """

    lms: LMS = models.ForeignKey(LMS, related_name="users", on_delete=models.CASCADE)
    """LMS on which the user belongs to."""

    lms_guid: str = models.CharField(max_length=200)
    """Identifier of the user on the LMS"""

    class Meta:
        verbose_name = 'lti user'
        verbose_name_plural = 'lti users'


    def __str__(self) -> str:
        return f'{self.user.get_full_name()} {self.lms_guid}'


class LTICourse(models.Model):
    """LTICourse Acts as the link between a course on a LMS
    and a course on PLaTon.
    """

    lms: LMS = models.ForeignKey(LMS, related_name="courses", on_delete=models.CASCADE)
    """LMS on which the course belongs to."""

    lms_guid: str = models.CharField(max_length=200)
    """Identifier of the course on the LMS."""


    class Meta:
        verbose_name = 'lti course'
        verbose_name_plural = 'lti courses'


    def __str__(self) -> str:
        return self.lms_guid
