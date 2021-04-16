from django.core.files.base import ContentFile
from django.db import models
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.db.models import Model
from django.contrib.auth.models import User
from rest_framework import serializers

from .ressources_storage import RessourceStorage
from .git_utils import GitUtils
from .file_utils import FilesUtils


class Resource(models.Model):
    """Resource """
    name = models.CharField(max_length=30, blank=True)
    path = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)
    tags = models.CharField(max_length=150, blank=True)

    def create_resource(self):
        """Create new repo with """
        GitUtils.create_repo(self.name)

    def tag(self):
        GitUtils.tag(self.name)


    def create_folder(self, pk: int, path: str):

        # TODO check s'il a le droit
        FilesUtils.create_folder(self.name, path)


    def delete_folder(self, pk: int, path: str):
        # TODO remove folders and files ....
        return
        # TODO check s'il a le droit
        # supprimer tous les files
        # FilesUtils.delete_folder(resource.name, path)
        # commit la resource


class Circle(Resource):
    """Represents a unique circle"""
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    users = models.ManyToManyField(User)


class File(models.Model):
    resource = models.ForeignKey(
        Resource,
        null=True,
        on_delete=models.CASCADE,
        related_name='files')
    document = models.FileField(storage=RessourceStorage())

    
    @classmethod
    def create_file(cls, id_resource, filename, content):
        """Filename est le relativepath depuis MEADIA ROOT"""
        try:
            resource = cls.objects.get(id=id_resource)
        except Resource.DoesNotExist:
            raise Resource.DoesNotExist
        
        new_file = cls.objects.create(resource=resource, document=None)
        new_file.document.save(filename, ContentFile(content))
        GitUtils.commit(resource.name, "update")
        return new_file


    def update_file(self, content: str):
        try:
            r = cls.objects.get(id=id_file)
        except cls.DoesNotExist:
            raise Resource.DoesNotExist
        with r.resource.open("w+") as f:
            f.write(content)
        GitUtils.commit(resource.name, "update")
    

    def __str__(self):
        return '%s: %s' % (self.document.name, self.document.path)
