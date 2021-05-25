import json
import logging
import os

from django.conf import settings
from django.core.management import BaseCommand
from pl_core.signals import create_defaults

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Django command to create default data before starting the server"""

    def handle(self, *args, **options):
        if settings.TESTING:
            return
        path = os.path.join(settings.SETTINGS_DIR, 'config.json')
        self.config = {}
        if os.path.exists(path):
            with open(path, 'r') as f:
                self.config = json.loads(f.read())
        create_defaults.send(self.__class__, config=self.config)
