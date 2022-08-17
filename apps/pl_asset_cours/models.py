from django.db import models

from django.contrib.auth import get_user_model

from pl_asset.models import Asset
from pl_asset.enums import AssetType

User = get_user_model()

class AssetCours(Asset):

    # Override field
    type = AssetType.COURS

    # Extra field
    description = models.CharField(max_length=1024, blank=True, null=True)
    properties = models.JSONField(default=dict, blank=True, null=True)
    content = models.JSONField(default=dict, blank=True, null= True)


class AssetCoursSession(models.Model):
    
    asset = models.ForeignKey(
        AssetCours,
        on_delete=models.SET_NULL,
        null=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    data = models.JSONField(default=dict, blank=True, null=True)