import os
import json
from asgiref.sync import async_to_sync

from django.db import models
from pl_asset.models import Asset
from pl_users.models import User
from pl_sandbox.models import Request, Sandbox

def default_response():
    return {}

class Runner(models.Model):

    asset = models.ForeignKey(Asset, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    builded = models.ForeignKey(Request, related_name='builder', null=True, on_delete=models.SET_NULL)
    response = models.JSONField(default=default_response)
    evaluated = models.ForeignKey(Request, related_name='evaluated', null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'''
            <Runner
                name="{self.asset.name}"
                user="{self.user.username}"
            >
        '''
    
    def get_user_path(self):
        pass

    def builder(self):
        sandbox = Sandbox.objects.first()

        base = self.asset.frozen.path
        path = os.path.join(base, 'data/content.tgz')
        export = os.path.join(os.path.join(base, self.user.username), 'build.tgz')
        config = {
            "commands" : [
                "python3 builder.py pl.json process.json"
            ],
            "path": path,
            "export": export,
            "result_path": "process.json"
        }

        self.builded : Request = async_to_sync(sandbox.assetor)(
            self.user,
            config
        )
    builded
    def evaluer(self):
        sandbox = Sandbox.objects.first()

        base = self.asset.frozen.path
        path = os.path.join(base, 'data/content.tgz')
        export = os.path.join(os.path.join(base, self.user.username), 'build.tgz')
        config = {
            "commands" : [
                "python3 eval.py pl.json process.json answer feedback"
            ],
            "path": path,
            "export": export,
            "result_path": "process.json"
        }

        self.evaluated : Request = async_to_sync(sandbox.execute)(
            self.user,
            config
        )  


    def render(self) -> dict:
        # TODO try except
        return json.loads(self.builded.response.result)
        

    @classmethod
    def build(cls, request, asset):
        runner = cls(asset=asset, user=request.user)
        runner.builder()
        return runner

    @classmethod
    def eval(cls, request, asset):
        runner = cls(asset=asset, user=request.user)
        runner.evaluer()
        return runner 
        
    
    @property
    def is_builded(self) -> bool:
        return self.builded and self.builded.success

    @property
    def is_evaluated(self) -> bool:
        return self.evaluated and self.evaluated.success
    
