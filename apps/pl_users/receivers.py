import logging

from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.dispatch.dispatcher import receiver
from pl_core.signals import create_defaults
from pl_lti.role import Role

logger = logging.getLogger(__name__)


@receiver(create_defaults)
def on_create_defaults(sender, config, **kwargs):
    logger.info('creating pl_users defaults')
    if 'admins' in config:
        for item in config['admins']:
            try:
                user = User.objects.create_user(
                    username=item['username'],
                    password=item['password']
                )
                user.is_staff = True
                user.is_admin = True
                user.is_superuser = True
                user.profile.role = Role.ADMINISTRATOR
                user.save()
                logger.info(f"User {item['username']} created")
            except IntegrityError:
                logger.warning(f"User '{item['username']}' already created")
                pass
