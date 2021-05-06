import os

from django.core.files.base import ContentFile
from django.contrib.postgres.fields import ArrayField
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
    publish = models.BooleanField(default = False)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='members')
    scientific_directors = models.ManyToManyField(User, related_name='scientifics')
    moderators = models.ManyToManyField(User, related_name='moderators')
    black_list = models.ManyToManyField(User, related_name='black-list')
    creator = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)

    def register(self, user):
        """Add a user to members in a circle."""
        this.members.add(user)
        this.moderators.remove(user)
        this.scientific_directors.remove(user)
        this.save()


    def kick(self, kicking, kicked):
        """user `kicking` kick user `kicked` out of the circle
        Raise an error if `kicking` don't have rights for kick."""
        # TODO check kicking rights
        this.members.remove(kicked)
        this.black_list.add(kicked)
        this.save()


    def publish(self, user):
        """Publish a circle. Raise an error if user don't have rights for praise."""
        self.publish = True
        self.save()


    def praise(self, user, user_praised, praise):
        """User `user` Praise user_praised to praise
        Raise an error if user don't have rights for praise."""
        # TODO check user rights
        if praise == 'MO':
            self.moderators.add(user_praised)
        elif praise == 'SD':
            self.scientific_directors.add(user_praised)
        else:
            raise ValueError



    def blame(self, user, user_blamed):
        """User `user` blame user_blamed to praise
        Raise an error if user don't have rights for blame."""
        if user.id != self.creator.id:
            raise ValueError
 
        this.moderators.remove(user_blamed)
        this.scientific_directors.remove(user_blamed)
        this.save()

    def parent(self, user, user_praised, praise):
        """User `user` Praise user_praised to praise
        Raise an error if user don't have rights for praise."""
        # Utile ?
        pass
    



class Resource(models.Model):
    """Resource """
    circle = models.ForeignKey(Circle, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    path = models.CharField(max_length=100, blank=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)


    def create_resource(self):
        """TODO REFACTOR - Create new repo with """
        GitUtils.create_repo(self.name)

    def tag(self):
        """TODO REFACTOR - """
        GitUtils.tag(self.name)

    def delete_folder(self, pk: int, path: str):
        """TODO REFACTOR - """
        return
        # supprimer tous les files
        # FilesUtils.delete_folder(resource.name, path)
        # commit la resource


class VersionStatus(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT'
        READY = 'READY'
        DEPRECATED = 'DEPRECATED'
        BUGGED = 'BUGGED'
        NOT_TESTED = 'NOT_TESTED'


    tag_git = models.CharField(max_length=50, blank=True)
    version = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT)
    tags = ArrayField(
            models.CharField(max_length=15, blank=True),
            size=8,
        )
    description = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_version(cls, resource):
        """Nous ne connaissons pas les files valides : 

        -  Nous pouvons avoir une liste de file ici ...
        -> Mais il y a des resources sans version.
            -> Donc pas les autoriser à faire de nouvelle version
        -> Beaucoup de duplication (5 versions ~= 5 fois le meme fichier)

        -  On pourrait dupliquer les informations et avoir une liste d'id en +
        -> C'est dur à maintenir

        """
        pass


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
