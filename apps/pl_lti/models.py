from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class LMS(models.Model):
    """
    Representation of a Learning Management System.

    Attributes:
        guid (str):
            GUID of the LMS corresponding to the
            tool_consumer_instance_guid parameter of the LTI request.
            Most of the time, it is the DNS of the LMS.
            For example:
            elearning.u-pem.fr.

        name (str):
            Name that identifies the LMS, for example: Moodle UPEM.

        url (str):
            URL of the LMS, for example: https://elearning.u-pem.fr/

        outcome_url (str):
            URL on which to post back results to a LMS.
            Correspond to the lis_outcome_service_url param of a LTI request

        client_id (str):
            Key that you'll need to enter on the LMS when creating a LTI activity.
            Correspond to the oauth_consumer_key param of a LTI request

        client_secret (str):
            Secret that you'll need to enter on the LMS when creating a LTI activity.
    """

    guid: str = models.CharField(max_length=200, blank=True, primary_key=True, unique=True)
    name: str = models.CharField(max_length=200)
    url: str = models.CharField(max_length=200)
    outcome_url: str = models.URLField(max_length=200)
    client_id: str = models.CharField(max_length=200)
    client_secret: str = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'LMS'


    def __str__(self) -> str:
        return "%s (%s)" % (self.name, self.url)


class LTIUser(models.Model):
    """
    LTIUser acts as the link between an user on a LMS
    and an user on PLaTon.

    Attributes:
        user (User):
            Reference to the PLaTon user related to this LTI user.

        lms (LMS):
            LMS on which the user belongs to.

        lms_user_id (int):
            Identifier of the user on the LMS
    """

    lms: LMS = models.ForeignKey(LMS, related_name="users", on_delete=models.CASCADE)
    user: User = models.ForeignKey(User, related_name="lti_users", on_delete=models.CASCADE)
    lms_user_id: str = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'LTI users'
        unique_together = ('lms', 'lms_user_id')


    def __str__(self) -> str:
        return f'{self.user.get_full_name()} {self.lms_user_id}'


class LTICourse(models.Model):
    """
    LTICourse Acts as the link between a course on a LMS
    and a course on PLaTon.

    Attributes:
        lms (LMS):
            LMS on which the course belongs to.

        lms_course_id (str):
            Identifier of the course on the LMS
    """

    lms: LMS = models.ForeignKey(LMS, related_name="courses", on_delete=models.CASCADE)
    lms_course_id: str = models.CharField(max_length=200)


    class Meta:
        verbose_name_plural = 'LTI courses'
        unique_together = ('lms', 'lms_course_id')



    def __str__(self) -> str:
        return self.lms_guid
