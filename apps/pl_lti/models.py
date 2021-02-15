from django.db import models
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404

# Create your models here.


class LMS(models.Model):
    """LMS model"""

    guid = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    outcome = models.URLField(max_length=200, null=True, blank=True)
    client_id = models.CharField(max_length=200, null=True, blank=True)
    client_secret = models.CharField(max_length=200, null=True, blank=True)


class LTIUser(models.Model):
    """LTIUser acts as the link between the LMS user and the Platon user  """
    
    pl_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    lsm_guid = models.CharField(max_length=200, null=True, blank=True)
    lms = models.ForeignKey(LMS, related_name="user_lms", on_delete=models.CASCADE)


class LTICourse(models.Model):
    """LTICourse Acts as the link between the LMSCourse and the Platoncourse"""
    
    lsm_guid = models.CharField(max_length=200, null=True, blank=True)
    lms = models.ForeignKey(LMS, related_name="course_lms", on_delete=models.CASCADE)
