from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models

from .utils import avatar_path, generate_identicon


class User(AbstractUser):
    """Extends User to save more informations about an user."""

    avatar = models.ImageField(upload_to=avatar_path, blank=True)
    is_editor = models.BooleanField('Editor', default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.pk and not self.avatar:
            self.avatar.save(self.username, File(generate_identicon(self)))

    @property
    def is_admin(self):
        """
        Returns whether the user is an administrator
        """
        return self.is_superuser or self.is_staff

    def __str__(self):
        return self.username
