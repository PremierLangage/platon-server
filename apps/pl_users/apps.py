from django.apps import AppConfig


class PlUsersConfig(AppConfig):
    name = 'pl_users'
    verbose_name = 'Users'

    def ready(self):
        from . import receivers  # keep to receive signals
