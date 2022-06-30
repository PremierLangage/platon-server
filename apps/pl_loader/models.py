import json
import os
import io
import tarfile
from asgiref.sync import async_to_sync

from django.db import models
from django.conf import settings
from . import utils

from .parser import Parser
from pl_resources.files import Directory
from pl_sandbox.models import Request, Sandbox

def default_content():
    return {}

def default_warnings():
    return { 'errors' : [] }

class Loader(models.Model):

    pl = models.JSONField(default=default_content)
    warnings = models.JSONField(default=default_warnings)
    status = models.BooleanField(verbose_name='status', default=False, null=False)

    def add_warning(self, error: str):
        self.warnings['errors'].append(error)

    def get_env(self, request, version) -> io.BytesIO:
        environment = io.BytesIO()
        with tarfile.open(fileobj=environment, mode="w:gz") as dest:
            # ADD INCLUDES IN TARGZ
            for includes in self.pl['__includes']:
                head, tail = os.path.split(includes['src_path'])
                try:
                    resource = Directory.get(head, request.user)
                    if resource.is_file(tail):
                        file = resource.read(tail, version, request=request)
                        tar_file, tar_info = utils.bytes_to_tarfile(includes['exp_path'], file)
                        dest.addfile(fileobj=tar_file, tarinfo=tar_info)
                    else:
                        self.add_warning('File %s not exist.' % tail)
                except FileNotFoundError as e:
                    self.add_warning('Resource %s not exist.' % head)
            # ADD PARSED JSON TO TARGZ
            json_file = json.dumps(self.pl, indent=4)
            tar_file, tar_info = utils.string_to_tarfile('pl.json', json_file)
            dest.addfile(fileobj=tar_file, tarinfo=tar_info)

        environment.seek(0)
        return environment

    @classmethod
    def get_loader(cls, request, directory, version, default_file = 'main.pl'):
        loader = Loader()
        loader.version = version
        
        try:
            dir = Directory.get(directory, request.user)
        except FileNotFoundError as e:
            loader.add_warning(f'Directory <{directory}> not found')
            return loader

        try:
            file = dir.read(default_file, version, request)
            if not isinstance(file, bytes):
                raise Exception(f'File <{default_file}> not found')
        except Exception as e:
            loader.add_warning(str(e))
            return loader
        
        try:
            parser = Parser(default_file, file)
            loader.pl, loader.warnings = parser.parse()
            if '__extends' in loader.pl:
                for extends in loader.pl['__extends']:
                    head, tail = os.path.split(extends)
                    extend_dir = Directory.get(head, request.user)
                    extend_file = extend_dir.read(tail, version)
                    extend_parser = Parser(tail, extend_file)
                    extend_pl, extend_warnings = extend_parser.parse()
                    utils.extends_dict(loader.pl, extend_pl)
                    loader.warnings += extend_warnings
        except Exception as e:
            loader.add_warning(str(e))
            return loader

        loader.status = True
        return loader

class Publisher(models.Model):
    
    loader = models.ForeignKey(Loader, related_name='publisher', null=True, on_delete=models.SET_NULL)
    path = models.CharField(max_length=1024, null=True)
    request = models.ForeignKey(Request, related_name='publisher', null=True, on_delete=models.SET_NULL)
    
    warnings = models.JSONField(default=default_warnings)
    status = models.BooleanField(verbose_name='status', default=False, null=False)

    def add_warning(self, error: str):
        self.warnings['errors'].append(error)

    @classmethod
    def get_publisher(cls, request, directory, version, loader : Loader):
        publisher = Publisher()
        publisher.loader = loader
        publisher.path = directory
        #publisher.path = os.path.join(settings.ASSETS_ROOT, directory)

        if not loader.status:
            publisher.warnings = loader.warnings
            return publisher

        environment = loader.get_env(request, version)

        try:
            nfs = os.path.join(settings.ASSETS_ROOT, os.path.join(publisher.path, 'tmp/content.tgz'))
            os.makedirs(os.path.dirname(nfs), exist_ok=True)
            
            with open(nfs, 'wb') as out:
                out.write(environment.read())

        except FileNotFoundError as e:
            environment.close()
            publisher.add_warning('Export environment on %s failed.' % nfs)
        
        publisher.status = True
        return publisher
    

    def build(self, request):
        if not self.status:
            return

        sandbox = Sandbox.objects.first()

        if not sandbox.enabled:
            self.add_warning('Sandbox are disable cannot process build')
            return
        
        self.loader.save()
        self.save()
        
        path = os.path.join(self.path, 'tmp/content.tgz')
        export = os.path.join(self.path, 'tmp/result.tgz')
        config = {
            "commands" : [
                "python3 builder.py pl.json process.json"
            ],
            "path": path,
            "export" : export,
            "result_path" : "process.json"
        }

        self.request : Request = async_to_sync(sandbox.assetor)(
            request.user,
            config
        )

        if self.request.success == False:
            self.status = False
            self.add_warning('Build request failed with error can not publish.')
            return

    def publish(self, request, version):
        if not self.status:
            return

        environment = self.loader.get_env(request, version)
        try:
            nfs = os.path.join(settings.ASSETS_ROOT, os.path.join(self.path, 'data/content.tgz'))
            os.makedirs(os.path.dirname(nfs), exist_ok=True)

            with open(nfs, 'wb') as out:
                out.write(environment.read())

        except FileNotFoundError as e:
            environment.close()
            self.add_warning('Export environment on %s failed.' % nfs)
        

# class Loader:

#     def __init__(self, name: str, directory: Directory, path: str, version: str):
#         if directory.is_file(path=path):
#             self.pl = dict()
#             self.warning = dict()
#             self.name = name
#             self.directory = directory
#             self.path = path
#             self.version = version
#         else:
#             raise LoaderInstenceException(f'Bad request : {path} is not file path.', status.HTTP_400_BAD_REQUEST)

    # def load(self, request) -> Tuple[dict, dict]:
    #     parser = Parser(self.path, self.directory.read(self.path, self.version, request=request))
    #     self.pl, self.warning = parser.parse()
    #     if '__extends' in self.pl:
    #         for extends in self.load_extends(request=request, version=self.version):
    #             loader, warning = extends.load(request=request, save=False)
    #             utils.extends_dict(self.pl, loader)
    #             self.warning += warning
        
    #     return self.pl, self.warning
        
#     def load_extends(self, request, version) -> Generator:
#         for extends in self.pl['__extends']:
#             head, tail = os.path.split(extends)
#             resource = Directory.get(head, request.user)
#             loader = Loader(resource,tail,version)
#             if loader is not None:
#                 yield loader

#     def load_publish(self, request, export):

#         env_io = io.BytesIO()
#         with tarfile.open(fileobj=env_io, mode="w:gz") as dest:
#             for includes in self.pl['__includes']:
#                 head, tail = os.path.split(includes['src_path'])
#                 try:
#                     resource = Directory.get(head, request.user)
#                     if resource.is_file(tail):
#                         file = resource.read(tail, self.version, request=request)
#                         tar_file, tar_info = utils.bytes_to_tarfile(includes['exp_path'], file)
#                         dest.addfile(fileobj=tar_file, tarinfo=tar_info)
#                         print("File added")
#                     else:
#                         self.warning.append('File %s not exist.' % tail)
#                 except FileNotFoundError as e:
#                     self.warning.append('Resource %s not exist.' % head)
#             self.publish_json(dest)

#         env_io.seek(0)
#         try:
#             with open(export, 'wb') as out:
#                 out.write(env_io.read())
#         except FileNotFoundError as e:
#             self.warning.append('Export environment on %s failed.' % export)

#     def publish_json(self, dest):
#         json_file = json.dumps(self.pl, indent=4)
#         tar_file, tar_info = utils.string_to_tarfile('pl.json', json_file)
#         dest.addfile(fileobj=tar_file, tarinfo=tar_info)

