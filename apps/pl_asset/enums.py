from django.db import models

class AssetType(models.TextChoices):

    COURS    = 'COURS'
    ACTIVITY = 'ACTIVITY'
    EXERCISE = 'EXERSICE'