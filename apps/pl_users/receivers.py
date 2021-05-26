import logging

from django.contrib.auth import get_user_model
from django.dispatch.dispatcher import receiver
from pl_core.signals import create_defaults

User = get_user_model()
logger = logging.getLogger(__name__)


@receiver(create_defaults)
def on_create_defaults(sender, config, **kwargs):
    logger.info('creating pl_users defaults')
    if 'users' in config:
        data = []
        for item in config['users']:
            user = User(
                username=item["username"],
                is_staff=bool(item.get('is_admin', False)),
                is_superuser=bool(item.get('is_admin', False)),
                is_editor=bool(item.get('is_editor', False)),
                email=item['email'],
                last_name=item['last_name'],
                first_name=item['first_name']
            )
            user.set_password("password")
            data.append(user)
        User.objects.bulk_create(data, ignore_conflicts=True)
