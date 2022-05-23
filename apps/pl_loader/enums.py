from django.db import models

class PublisherStatus(models.TextChoices):
    ERR_LOADERER = 'ERR_LOADERER'
    ERR_EXPORT = 'ERR_EXPORT'
    ERR_PUBLISH  = 'ERR_PUBLISH'