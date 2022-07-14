import os
import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from .enums import AssetType

ASSETS = settings.ASSETS_ROOT

User = get_user_model()

# Create your models here.
class Asset(models.Model):

    path = models.CharField(max_length=1024, primary_key=True)
    name = models.SlugField(max_length=25, unique=True)
    type = models.CharField(max_length=20, choices=AssetType.choices)
    properties = models.JSONField(default=dict, blank=True, null=True)
    content = models.JSONField(default=dict, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self) -> str:
        return f'''
            <Asset
                type="{self.type}"
                name="{self.path}"
            >
        '''

class RunnableAsset(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        null=False
    )

    @property
    def location(self) -> str:
        return self.asset.path

    def get_env(self):
        pass

    def get(self, request, *args, **kwargs):
        (session, flag) = RunnableAssetSession.objects.get_or_create(asset=self,user=request.user)
        session.build()
        return session.content()

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
        return True
    
    @property
    def is_grader(self):
        return False

    class Meta:
        unique_together = ('asset', 'user', 'session_id')

    def content(self) -> dict:
        if not self.is_build:
            return ''

        base = os.path.join(ASSETS, self.asset.location)
        path = os.path.join(base, os.path.join(self.user.username, "0bb2efc2-0569-4679-8fb6-c71985338534"))
        file = os.path.join(path, "process.json")

        with open(file) as process:
            content = process.read()
        
        return json.loads(content)
        

    def build(self):
        if self.is_build:
            return
        return

    def eval(self):
        pass