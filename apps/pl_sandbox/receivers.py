import json
import logging
import sys

from django.apps import apps
from django.conf import settings
from django.db.models.signals import post_migrate
from django.db.utils import IntegrityError
from django.dispatch.dispatcher import receiver
from pl_core.signals import create_defaults

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def setup_celery_tasks(sender, *args, **kwargs):
    """Do some checks when django starts.

    * SANDBOX_POLL_USAGE_EVERY settings in an integer above 15.
    * SANDBOX_POLL_SPECS_EVERY settings is an integer above 300.
    * Every existing "poll usage" periodic task are done every
        SANDBOX_POLL_SPECS_EVERY.
    * Every existing "poll specifications" periodic task are done every
        SANDBOX_POLL_USAGE_EVERY.
    * Every existing Sandbox have a period task for "poll usage" and
        "poll specification"
    """

    if {"makemigrations", "migrate", "reset_db"}.intersection(sys.argv):
        return

    # Check settings
    if (not isinstance(settings.SANDBOX_POLL_USAGE_EVERY, int)
            or settings.SANDBOX_POLL_USAGE_EVERY < 15):
        raise ValueError(
            f"Incorrect SANDBOX_POLL_USAGE_EVERY settings:{settings.SANDBOX_POLL_USAGE_EVERY}"
        )
    if (not isinstance(settings.SANDBOX_POLL_SPECS_EVERY, int)
            or settings.SANDBOX_POLL_SPECS_EVERY < 300):
        raise ValueError(
            f"Incorrect SANDBOX_POLL_SPECS_EVERY settings:{settings.SANDBOX_POLL_SPECS_EVERY}"
        )

    # Load needed models
    PeriodicTask = apps.get_model(app_label='django_celery_beat', model_name='PeriodicTask')
    IntervalSchedule = apps.get_model(
        app_label='django_celery_beat', model_name='IntervalSchedule'
    )
    Sandbox = apps.get_model(app_label='pl_sandbox', model_name='Sandbox')

    # Retrieving / creating schedules needed for periodic tasks
    usage_schedule, created = IntervalSchedule.objects.get_or_create(
        every=settings.SANDBOX_POLL_USAGE_EVERY, period=IntervalSchedule.SECONDS
    )
    specs_schedule, created = IntervalSchedule.objects.get_or_create(
        every=settings.SANDBOX_POLL_SPECS_EVERY,
        period=IntervalSchedule.SECONDS
    )

    # Updating every existing periodic tasks so that they correspond to
    # SANDBOX_POLL_USAGE_EVERY & SANDBOX_POLL_SPECS_EVERY
    PeriodicTask.objects.filter(
        name__startswith="sandbox_poll_usage"
    ).update(interval=usage_schedule.pk)
    PeriodicTask.objects.filter(
        name__startswith="sandbox_poll_specifications"
    ).update(interval=specs_schedule.pk)

    # Checking that every sandbox has corresponding periodic tasks
    for sandbox in Sandbox.objects.all():
        task_name = f"sandbox_poll_usage_{sandbox.pk}"
        try:
            PeriodicTask.objects.get(name=task_name)
        except PeriodicTask.DoesNotExist:
            logger.info(f"Creating periodic task to poll usage of sandbox {sandbox}")
            PeriodicTask.objects.create(
                name=task_name, interval=usage_schedule, task='pl_sandbox.tasks.poll_usage',
                args=json.dumps([sandbox.pk])
            )

        task_name = f"sandbox_poll_specifications_{sandbox.pk}"
        try:
            PeriodicTask.objects.get(name=task_name)
        except PeriodicTask.DoesNotExist:
            logger.info(f"Creating periodic task to poll specifications of sandbox {sandbox}")
            PeriodicTask.objects.create(
                name=task_name, interval=specs_schedule, args=json.dumps([sandbox.pk]),
                task='pl_sandbox.tasks.poll_specifications',
            )


@receiver(create_defaults)
def on_create_defaults(sender, config, **kwargs):
    logger.info('creating pl_sandbox defaults')
    Sandbox = apps.get_model(app_label='pl_sandbox', model_name='Sandbox')
    sandbox, created = Sandbox.objects.get_or_create(
        name="Default",
        url=settings.SANDBOX_URL,
        enabled=True
    )
    sandbox.url = settings.SANDBOX_URL
    sandbox.save()
