import logging

from django.db.utils import IntegrityError
from django.dispatch.dispatcher import receiver
from pl_core.signals import create_defaults

from pl_lti.models import LMS

logger = logging.getLogger(__name__)


@receiver(create_defaults)
def on_create_defaults(sender, config, **kwargs):
    logger.info('creating pl_lti defaults')
    if 'lms' in config:
        logger.info('creating default LMS')
        for item in config['lms']:
            try:
                LMS.objects.create(
                    guid=item['guid'],
                    name=item['name'],
                    url=item['url'],
                    outcome_url=item['outcome_url'],
                    client_id=item['client_id'],
                    client_secret=item['client_secret']
                )
                logger.info(f"LMS {item['name']} created")
            except IntegrityError:
                logger.warning(f"LMS '{item['name']}' already created")
                pass
