from django.apps import AppConfig


class PlLtiConfig(AppConfig):
    name = 'pl_lti'
    verbose_name = 'LTI'

    def ready(self):
        from . import receivers  # keep to receive signals
