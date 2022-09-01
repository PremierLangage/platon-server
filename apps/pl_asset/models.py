from email.policy import default
import os
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model

from .types import AssetType

User = get_user_model()

class Asset(models.Model):

    path = models.CharField(max_length=1024, unique=True, null=False)
    name = models.SlugField(max_length=25, unique=True, primary_key=True)
    type = models.CharField(max_length=20, choices=AssetType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        editable=False,
        on_delete=models.SET_NULL,
        null=True
    )
    parent = models.ForeignKey(
        'Asset',
        on_delete=models.SET_NULL,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.parent:
            self.path = os.path.join(self.parent.path, self.name)
        else:
            self.path = self.name
        super(Asset, self).save(*args, **kwargs)
        try:
            assets = Asset.objects.filter(parent=self)
            for asset in assets:
                asset.save()
        except Asset.DoesNotExist:
            pass

class AssetCours(models.Model):

    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        editable=False
    )

    description = models.CharField(max_length=1024, default='', blank=True, null=False)
    content = models.JSONField(default=dict, null=False)

class AssetActivity(models.Model):

    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        editable=False
    )
    content = models.JSONField(default=dict, null=False)

class AssetExersice(models.Model):

    asset = models.OneToOneField(
        Asset,
        on_delete=models.CASCADE,
        editable=False
    )
    content = models.JSONField(default=dict, null=False)
