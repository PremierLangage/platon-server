from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_init

from .enums import PropertyName
from pl_resources.enums import ResourceTypes
from pl_resources.models import Resource
from pl_loader.models import Publisher

import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from nfs_asset import *

ASSETS = settings.ASSETS_ROOT

User = get_user_model()

class Asset(models.Model):
    """
    Asset model 
    """

    slug_name = models.CharField(max_length=50, null=False, unique=True)
    type = models.CharField(max_length=50, null=False, choices=ResourceTypes.choices) # Should go to FR
    parent = models.ForeignKey('Asset', null=True, on_delete=models.SET_NULL)
    date_creation = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    frozen_resource = models.ForeignKey(Publisher, related_name='publisher', null=False, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, null=True)

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self) -> str:
        return f'''
            <Asset
                type="{self.type}"
                name="{self.slug_name}"
            >
        '''


class AssetProperties(models.Model):
    
    asset = models.ForeignKey(Asset, null=False, on_delete=models.CASCADE)
    property_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    property_id = models.PositiveBigIntegerField()
    property = GenericForeignKey('property_type', 'property_id')

class FrozenRessource(models.Model):
    resource = models.ForeignKey(Resource, related_name='resource', null=True, on_delete=models.SET_NULL)
    resource_version = models.CharField(max_length=50, default='master')
    path = models.CharField(max_length=255, null=True)

class Properties(models.Model):
    """
    Properties model 
    """

    property_type = models.CharField(choices=PropertyName.choices, max_length=50, null=True)
    property = models.JSONField(null=False)

class RunnableAsset(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        null=False
    )

    @property
    def location(self) -> str:
        return self.asset.slug_name

    def get_env(self, user : User) -> Path:
        return Path(get_path_user(self.asset, user), "env")

    # def get_or_create_session(self, user):
    #     session = RunnableAssetSession.objects.get_or_create(asset=self, user=user)
    #     return session

class RunnableAssetSession(models.Model):

    asset = models.ForeignKey(
        RunnableAsset,
        on_delete=models.SET_NULL,
        null=True
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    session_id = models.CharField(
        max_length=36,
        blank=False,
        null=True
    )

    @property
    def is_build(self):
        return False
    
    @property
    def is_grader(self):
        return False

    class Meta:
        unique_together = ('asset', 'user', 'session_id')

    def render(self):
        pass

    def build(self):
        base = os.path.join(ASSETS, self.asset.location)
        path = os.path.join(base, os.path.join(self.user.username, "0bb2efc2-0569-4679-8fb6-c71985338534"))
        file = os.path.join(path, "process.json")
        return file

    def eval(self):
        pass
