from dataclasses import asdict
import os, io, tarfile, json
from asgiref.sync import async_to_sync

from django.contrib.auth import get_user_model
from rest_framework.request import Request

from pl_resources.models import Resource
from pl_resources.files import Directory
from pl_resources.enums import ResourceTypes
from pl_sandbox.models import Sandbox

from . import exceptions, utils
from .parser.parser import Parser

from platonparser.parser.parser import parse_file
from platonparser.parser.utils import base_get_location, FullPath
from platonparser.parser.parser_exceptions import ParserException


User = get_user_model()

class Loader:

    def __init__(self, resource: Resource, directory: Directory, version: str, user: User):
        """Representation of loaded resource.
        """
        self.resource = resource
        self.directory = directory
        self.version = version
        self.user = user
        self.json = dict
        self.parsed = False
        self.build_request = None

    @property
    def environment(self) -> str:
        if self.build_request is not None:
            return self.build_request.response.environment
        return ''

    @classmethod
    def get(cls, request: Request, resource_id: int) -> 'Loader':
        """Get loader instance of resource
        
        Raises:
            
        """
        if not request.user.is_authenticated:
            raise exceptions.LoaderInitErrorUserNotAuthanticated()

        try:
            resource: Resource = Resource.objects.get(pk=resource_id)
        except Resource.DoesNotExist:
            raise exceptions.LoaderInitErrorResourceDoesNotExist()
        
        if not resource.is_loadable_by(request.user):
            raise exceptions.LoaderInitErrorUserNotPermit()
        
        try:
            directory: Directory = Directory.get(resource.dir_name, request.user)
        except FileNotFoundError:
            raise exceptions.LoaderInitErrorResourceDirectoryDoesNotExist()

        # query_params = request.query_params
        # version = query_params.get('version', 'master')
        version = 'master'
        
        return cls(resource, directory, version, request.user)

    def get_env(self) -> io.BytesIO:
        """
        Returns in binary form a tar file containing the environnement of the resource.
        Must have been parsed before.
        """
        if not self.parsed:
            raise exceptions.LoaderStateError()
        environment = io.BytesIO()
        with tarfile.open(fileobj=environment, mode="w:gz") as env:
            for includes in self.json['__includes']:
                head, tail = os.path.split(includes['src_path'])
                if self.directory.is_file(tail):
                    file = self.directory.read(tail, self.version)
                    tar_file, tar_info = utils.bytes_to_tarfile(includes['exp_path'], file)
                    env.addfile(fileobj=tar_file, tarinfo=tar_info)
                else:
                    self.warnings['errors'].append('File %s not exist.' % tail)
            json_file = json.dumps(self.json, indent=4)
            tar_file, tar_info = utils.string_to_tarfile('pl.json', json_file)
            env.addfile(fileobj=tar_file, tarinfo=tar_info)

        environment.seek(0)
        return environment

    def build(self, sandbox: Sandbox, config: dict):
        environment = self.get_env()
        self.build_request = async_to_sync(sandbox.execute)(
            self.user,
            config,
            environment
        )
        if environment is not None:
            environment.close()

    def parse(self):
        if self.resource.type == ResourceTypes.EXERCISE:
            if not self.parse_pl():
                raise exceptions.LoaderParseError()
        elif self.resource.type == ResourceTypes.ACTIVITY:
            self.parse_pla()
        else:
            raise exceptions.LoaderParseError()
        self.parsed = True

    def parse_pl(self):
        """Parses the main file of a pl resource"""
        try:
            self.directory.exists('main.pl')
            self.directory.is_file('main.pl')
            file = self.directory.read('main.pl', self.version)
        except (TypeError, PermissionError):
            raise exceptions.LoaderParseError()

        try:
            output = parse_file(file, FullPath(self.resource.id, "/main.pl"), self.resource.circle.id,
                                base_get_location)
            self.json = asdict(output) 
        except ParserException as e:
            raise e

        return True

    # def parse_pl(self) -> bool:
    #     try:
    #         self.directory.exists('main.pl')
    #         self.directory.is_file('main.pl')
    #         file = self.directory.read('main.pl', self.version)
    #     except (TypeError, PermissionError):
    #         raise exceptions.LoaderParseError()
        
    #     try:
    #         parser = Parser('main.pl', file)
            # self.json, self.warnings = parser.parse()
    #         if '__extends' in self.json:
    #             for extends in self.json['__extends']:
    #                 head, tail = os.path.split(extends)
    #                 extends_file = Directory.get(head, self.user).read(tail, self.version)
    #                 extends_json, extends_warnings = Parser(tail, extends_file).parse()
    #                 utils.extends_dict(self.json, extends_json)
    #                 self.warnings += extends_warnings
    #     except Exception as e:
    #         self.warnings['errors'].append(str(e))
    #         return False
        
    #     return True

    def parse_pla(self):
        pass
        
        