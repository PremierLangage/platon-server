from pathlib import Path
from typing import Optional

from django.conf import settings
from django.contrib.auth import get_user_model

import os

from .models import Asset


NFS_ASSETS = settings.ASSETS_ROOT

def get_asset_from_path(path : Path) -> Optional[Asset] : # Optional[Asset] = Asset | None
    query = Asset.objects.get(path=path.absolute)
    if len(query) < 1 : 
        return Optional()
    return Optional(query[1])

class AssetVisitor():

    def get_root():
        a = Asset()
        a.path = NFS_ASSETS
        return a

    def visit(self, node):
        method = "visit_" + node.type
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_course(self, node):
        self.visit(node)
        print("visiting course : " + node.path)


    def visit_activity(self, node):
        self.visit(node)
        print("visiting activity : " + node.path)


    def visit_exercice(self, node):
        self.visit(node)
        print("visiting exercice : " + node.path)


    def generic_visit(self, node) :
        for c in  os.listdir(node.path):
            path = Path(node.path, c)

            if not os.path.isdir(path) : continue

            child = get_asset_from_path(path)
            if child : self.visit(child)


def _get_or_create_path(path : Path):
    if not os.path.exists(path): os.mkdir(path)
    return path

def get_root_path_for(asset : Asset) -> Path : 
    path : Path = Path(asset.parent.path, asset.slug)
    return _get_or_create_path(path) 

def get_path_user(asset : Asset, user : get_user_model()) -> Path:
    path : Path = Path(asset.path, user.last_name + user.name + user.id)
    #TODO copy environment into user directory


    return _get_or_create_path(path)

