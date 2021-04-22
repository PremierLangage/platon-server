import os

from django.core.files.base import ContentFile
from django.db import models
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from django.db.models import Model
from django.conf import settings


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
    def create_file(cls, id_resource, filename, path, content):
        """Filename est le relativepath depuis MEADIA ROOT"""
        try:
            resource = Resource.objects.get(id=id_resource)
        except Resource.DoesNotExist:
            raise Resource.DoesNotExist
        # relative path from repo
        relative_path = os.path.join(resource.name, path)
        # create folder if is needed
        FilesUtils.create_folder(relative_path)
        
        real_filename = os.path.join(relative_path, filename)

        new_file = cls.objects.create(resource=resource, document=None)
        new_file.document.save(real_filename, ContentFile(content))
        GitUtils.commit(resource.name, "update")
        return new_file


    def update_file(self, content: str):
        """ update file"""
        RessourceStorage.update(self.document, content)
        GitUtils.commit(resource.name, "update")

    
    def get_file(self):
        """return content of the file. And crete file is not exist"""
        return {self.document.name: RessourceStorage.open_file(self.document)}
    

    def delete(self, *args, **kwargs):
        self.__delete_file()
        super().delete(*args, **kwargs)

    def __delete_file(self):
        """delete file and directory if he is empty"""
        sep = "/"
        tab = self.document.name.split(sep)
        path_folder = sep.join(tab[:-1])
        FilesUtils.delete_file(self.document.name)
        # Check if relative path is not root
        if path_folder:
            FilesUtils.delete_folder(path_folder)
        GitUtils.commit(resource.name, "delete")


    def __str__(self):
        return '%s: %s' % (self.document.name, self.document.path)
