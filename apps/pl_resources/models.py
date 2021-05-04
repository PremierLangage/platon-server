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




class Circle(models.Model):
    """Represents a unique circle"""
    publish = models.BooleanField(default = False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    scientific_directors = models.ManyToManyField(User)
    moderators = models.ManyToManyField(User)
    creator = models.ForeignKey(User, null=False)
    date = models.DateTimeField(auto_now_add=True)



class Resource(models.Model):
    """Resource """
    name = models.CharField(max_length=30, blank=True)
    path = models.CharField(max_length=100, blank=True)
    creator = models.ForeignKey(User, null=False)
    date = models.DateTimeField(auto_now_add=True)


    def create_resource(self):
        """TODO REFACTOR - Create new repo with """
        GitUtils.create_repo(self.name)

    def tag(self):
        """TODO REFACTOR - """
        GitUtils.tag(self.name)

    def delete_folder(self, pk: int, path: str):
        """TODO REFACTOR - """
        # TODO remove folders and files ....
        return
        # TODO check s'il a le droit
        # supprimer tous les files
        # FilesUtils.delete_folder(resource.name, path)
        # commit la resource


class VersionStatus(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DRAFT'
        READY = 'READY'
        DEPRECARED = 'DEPRECARED'
        BUGGED = 'BUGGED'
        NOT_TESTED = 'NOT_TESTED'

    tag_git = models.CharField(max_length=50, blank=True)
    version = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT)
    description = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)




class File(models.Model):
    resource = models.ForeignKey(
        Resource,
        null=True,
        on_delete=models.CASCADE,
        related_name='files')
    document = models.FileField(storage=RessourceStorage())

    
    @classmethod
    def create_file(cls, id_resource, filename, path, content):
        """TODO REFACTOR - Filename est le relativepath depuis MEADIA ROOT"""
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
        """TODO REFACTOR -  update file"""
        RessourceStorage.update(self.document, content)
        GitUtils.commit(resource.name, "update")

    
    def get_file(self):
        """TODO REFACTOR - return content of the file. And crete file is not exist"""
        return {self.document.name: RessourceStorage.open_file(self.document)}
    

    def delete(self, *args, **kwargs):
        """TODO REFACTOR - """
        self.__delete_file()
        super().delete(*args, **kwargs)

    def __delete_file(self):
        """TODO REFACTOR - delete file and directory if he is empty"""
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
