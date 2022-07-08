import os
import json
from asgiref.sync import async_to_sync

from django.db import models
from pl_asset.models import Asset
from pl_users.models import User
from pl_sandbox.models import Request, Sandbox

def default_response():
    return {}

    
