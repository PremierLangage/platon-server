import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from pl_core.signals import create_defaults

from pl_resources.enums import CircleTypes
from pl_resources.models import Circle, Level, Member

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Member)
def on_save_member(sender, instance: Member, created: bool, **kwargs):
    logger.info(f'adding member to circle watchers')
    if created:
        instance.circle.watchers.add(instance.user)
        instance.circle.save()


@receiver(post_delete, sender=Member)
def on_delete_member(sender, instance: Member, **kwargs):
    logger.info(f'removing member to circle watchers')
    instance.circle.watchers.remove(instance.user)


@receiver(create_defaults)
def on_create_defaults(sender, config, **kwargs):
    logger.info(f'creating pl_resources defaults')

    Circle.objects.get_or_create(
        type=CircleTypes.PUBLIC,
        parent=None,
        defaults={
            'name': 'Général',
            'desc': 'Cercle principal de la plateforme.'
        }
    )

    Level.objects.bulk_create([
        Level(name="6e"),
        Level(name="5e"),
        Level(name="4e"),
        Level(name="3e"),
        Level(name="2nd"),
        Level(name="1ère"),
        Level(name="Terminal"),
        Level(name="L1"),
        Level(name="L2"),
        Level(name="M1"),
        Level(name="M2"),
        Level(name="DUT 1"),
        Level(name="DUT 2"),
        Level(name="BTS 1"),
        Level(name="BTS 2"),
    ], ignore_conflicts=True)
