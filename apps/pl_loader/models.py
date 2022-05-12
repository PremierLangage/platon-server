import json
import os
import io
import tarfile

from typing import Tuple, Generator
from django.db import models
from jsonfield import JSONField
from rest_framework import status

from . import utils

from .exceptions import LoaderInstenceException, LoaderStateException
from .parser import Parser
from pl_resources.files import Directory

# Create your models here.

class Loader:

    def __init__(self, name: str, directory: Directory, path: str, version: str):
        if directory.is_file(path=path):
            self.pl = dict()
            self.warning = dict()
            self.name = name
            self.directory = directory
            self.path = path
            self.version = version
        else:
            raise LoaderInstenceException(f'Bad request : {path} is not file path.', status.HTTP_400_BAD_REQUEST)

    def load(self, request) -> Tuple[dict, dict]:
        parser = Parser(self.path, self.directory.read(self.path, self.version, request=request))
        self.pl, self.warning = parser.parse()
        if '__extends' in self.pl:
            for extends in self.load_extends(request=request, version=self.version):
                loader, warning = extends.load(request=request, save=False)
                utils.extends_dict(self.pl, loader)
                self.warning += warning
        
        return self.pl, self.warning
        
    def load_extends(self, request, version) -> Generator:
        for extends in self.pl['__extends']:
            head, tail = os.path.split(extends)
            resource = Directory.get(head, request.user)
            loader = Loader(resource,tail,version)
            if loader is not None:
                yield loader

    def load_publish(self, request, export):

        env_io = io.BytesIO()
        with tarfile.open(fileobj=env_io, mode="w:gz") as dest:
            for includes in self.pl['__includes']:
                head, tail = os.path.split(includes['src_path'])
                try:
                    resource = Directory.get(head, request.user)
                    if resource.is_file(tail):
                        file = resource.read(tail, self.version, request=request)
                        tar_file, tar_info = utils.bytes_to_tarfile(includes['exp_path'], file)
                        dest.addfile(fileobj=tar_file, tarinfo=tar_info)
                        print("File added")
                    else:
                        self.warning.append('File %s not exist.' % tail)
                except FileNotFoundError as e:
                    self.warning.append('Resource %s not exist.' % head)
            self.publish_json(dest)

        env_io.seek(0)
        try:
            with open(export, 'wb') as out:
                out.write(env_io.read())
        except FileNotFoundError as e:
            self.warning.append('Export environment on %s failed.' % export)

    def publish_json(self, dest):
        json_file = json.dumps(self.pl, indent=4)
        tar_file, tar_info = utils.string_to_tarfile('pl.json', json_file)
        dest.addfile(fileobj=tar_file, tarinfo=tar_info)

