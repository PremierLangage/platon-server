from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from .enums import AssetType

ASSETS = settings.ASSETS_ROOT

User = get_user_model()

class Asset(models.Model):

    class Meta:
        abstract = True

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

    def __str__(self) -> str:
        return f'''
            <Asset
                type="{self.type}"
                name="{self.name}"
            >
        '''
    