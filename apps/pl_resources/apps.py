from django.apps import AppConfig


class PlResourcesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pl_resources'

    def ready(self):
        from . import receivers  # keep to receive signals
