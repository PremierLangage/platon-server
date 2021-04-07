import json
import logging
import os

import django
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from pl_sandbox.models import Sandbox
from pl_lti.models import LMS
from pl_lti.role import Role

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Django command to pause execution until db is available"""
 
    def handle(self, *args, **options):
        path = os.path.join(settings.SETTINGS_DIR, 'config.json')
        if not os.path.exists(path):
            return

        with open(path, 'r') as f:
            self.config = json.loads(f.read())

        self.create_lms()
        self.create_admins()
        self.create_sandboxes()


    def create_lms(self):
        if 'lms' in self.config:
            logger.info('creating default LMS')
            for item in self.config['lms']:
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
                except django.db.utils.IntegrityError:
                    logger.warning(f"LMS '{item['name']}' already created")
                    pass


    def create_admins(self):
        # Create admins
        if 'admins' in self.config:
            logger.info('creating default admin users')
            for item in self.config['admins']:
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
                except django.db.utils.IntegrityError:
                    logger.warning(f"User '{item['username']}' already created")
                    pass


    def create_sandboxes(self):
        if 'sandboxes' in self.config:
            logger.info('creating default sanboxes')
            for item in self.config['sandboxes']:
                try:
                    Sandbox.objects.create(
                        name=item['name'],
                        url=item['url'],
                        enabled=item['enabled'],
                    )
                    logger.info(f"Sandbox {item['name']} created")
                except django.db.utils.IntegrityError:
                    logger.warning(f"Sandbox '{item['name']}' already created")
                    pass
