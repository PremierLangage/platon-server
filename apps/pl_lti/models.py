from django.db import models
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404

# Create your models here.



class LTIModel(models.Model):
    """Mixin for models that can be created through LTI.
    
    This Mixin add an optionnal id corresponding to the ID of the object on the consumer's server
    and the name of the consumer itself must be a key of settings.LTI_OAUTH_CREDENTIALS.
    """
    
    CONSUMER = ((i, i) for i in settings.LTI_OAUTH_CREDENTIALS.keys())
    consumer_id = models.CharField(max_length=200, null=True, blank=True)
    consumer = models.CharField(max_length=200, choices=CONSUMER, null=True, blank=True)
    
    
    class Meta:
        abstract = True
        unique_together = ("consumer", "consumer_id")
