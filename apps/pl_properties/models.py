from rest_framework.reverse import reverse
from django.db import models
from . import enums

class Properties(models.Model):

    class Meta:
        abstract = True
    
    def get_type(self) -> enums.PropertiesTypes:
        raise NotImplementedError

    def get_url(self, request, *args, **kwargs):
        return reverse(
            f'pl_properties:{self.get_type().value}-detail',
            request=request,
            kwargs=kwargs
        )

class DescriptionProperty(Properties):
    
    content = models.CharField(max_length=1024, null=False, blank=False)

    def get_type(self) -> enums.PropertiesTypes:
        return enums.PropertiesTypes.DESCRIPTION
