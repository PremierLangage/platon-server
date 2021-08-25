import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from pl_core.signals import create_defaults

from pl_resources.files import Directory
from pl_resources.models import Circle, Level, Member, Topic

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

    general, created = Circle.objects.get_or_create(
        parent=None,
        defaults={
            'name': 'Général',
            'desc': 'Cercle principal de la plateforme.'
        }
    )
    if created:
        Directory.create(f'circle:{general.pk}')

    draft, created = Circle.objects.get_or_create(
        parent=general,
        name='Drafts',
        defaults={
            'name': 'Drafts',
            'opened': True,
            'desc': 'Cercle ouvert pour faire des essais.'
        }
    )

    if created:
        Directory.create(f'circle:{draft.pk}')

    levels = config.get('levels', [])
    Level.objects.bulk_create(
        [Level(name=item) for item in levels],
        ignore_conflicts=True
    )

    topics = config.get('topics', [])
    Topic.objects.bulk_create(
        [Topic(name=item) for item in topics],
        ignore_conflicts=True
    )
