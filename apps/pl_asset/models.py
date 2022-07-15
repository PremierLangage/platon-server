import os
import json
import io
import tarfile

from typing import Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from asgiref.sync import async_to_sync

from .enums import AssetType
from . import exceptions

from pl_sandbox.models import Sandbox, Request

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

    def get_env(self) -> Optional[io.BytesIO]:
        environment = io.BytesIO()

        base = os.path.join(ASSETS, self.location)
        env = os.path.join(base, 'env')

        if not os.path.isdir(env):
            return None


        with tarfile.open(fileobj=environment, mode="w:gz") as tar:
            for fn in os.listdir(env):
                p = os.path.join(env, fn)
                tar.add(p, arcname=fn)
        
        environment.seek(0)
        return environment

    def content(self, request, *args, **kwargs):
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
        if not self.session_id:
            return False
        base = os.path.join(ASSETS, self.asset.location)
        path = os.path.join(base, os.path.join(self.user.username, self.session_id))
        process = os.path.join(path, "process.json")
        
        if not os.path.isfile(process):
            return False
        return True
    
    @property
    def is_grader(self):
        return False

    class Meta:
        unique_together = ('asset', 'user', 'session_id')

    def content(self) -> dict:
        if not self.is_build:
            return {'build': 'NOT BUILD'}
        
        if not self.session_id:
            return {'build': 'SESSION ID MISSING'}

        base = os.path.join(ASSETS, self.asset.location)
        path = os.path.join(base, os.path.join(self.user.username, self.session_id))
        file = os.path.join(path, "process.json")

        with open(file) as process:
            content = process.read()
        
        return json.loads(content)
        

    def build(self):
        
        if self.is_build:
            return

        environment = self.asset.get_env()

        try:
            sandbox = Sandbox.objects.first()
        except Sandbox.DoesNotExist:
            raise exceptions.SandboxNotFoundError

        if not sandbox.enabled:
            raise exceptions.SandboxDisabledError
        
        request: Request = async_to_sync(sandbox.execute)(
            user=self.user,
            config={
                "commands" : [
                    "python3 builder.py pl.json process.json"
                ],
                "result_path" : "process.json"
            },
            environment=environment
        )

        self.session_id = request.response.environment
        self.save()

        base = os.path.join(ASSETS, self.asset.location)
        path = os.path.join(base, os.path.join(self.user.username, self.session_id))
        process = os.path.join(path, "process.json")

        os.makedirs(os.path.dirname(process), exist_ok=True)

        with open(process, mode="w") as file:
            file.write(request.response.result)

        environment.close()

    def eval(self):
        pass