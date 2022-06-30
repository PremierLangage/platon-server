from django.db import models

class AssetType(models.TextChoices):
    EXERCICE = 'EXERCICE'
    ACTIVITY = 'ACTIVITY'
    COURS = 'COURS'