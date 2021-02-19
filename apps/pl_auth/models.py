from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from enumfields import EnumIntegerField

from .enums import Role


class Profile(models.Model):
    """Extends User to save more informations about an user."""

    user: User = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role: Role = EnumIntegerField(Role, default=Role.LEARNER)


    def is_admin(self):
        """
        Returns whether the user is an administrator
        (Role or django su / staff).
        """
        return self.user.is_superuser or self.user.is_staff or self.role == Role.ADMINISTRATOR


    def is_teacher(self):
        """Returns whether the user is a teacher"""
        return self.role in Role.TEACHING_STAFF_ROLES


    def save(self, *args, **kwargs):
        """Saves the profile to the database"""

        # Fix the IntegrityError when creating
        # a new user and modifying default profile.
        if self.pk is None:
            p = Profile.objects.filter(user=self.user)
            p.delete()
            super(Profile, self).save(*args, **kwargs)
        else:
            super(Profile, self).save(*args, **kwargs)


    def __str__(self):
        return self.user.username + "'s Profile"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance: User, created, **kwargs):
    """When a new user is saved, create or save it's corresponding profile."""
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
