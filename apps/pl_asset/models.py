from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_init

from .enums import PropertyName
from pl_resources.enums import ResourceTypes
from pl_resources.models import Resource
from pl_loader.models import Publisher

class Asset(models.Model):
    """
    Asset model 
    """

    slug = models.CharField(max_length=50, null=False, unique=True)
    type = models.CharField(max_length=50, null=False, choices=ResourceTypes.choices)
    parent = models.ForeignKey('Asset', null=True, on_delete=models.SET_NULL)
    date_creation = models.DateField(auto_now_add=True)
    frozen_resource = models.ForeignKey(Publisher, related_name='publisher', null=False, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

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
