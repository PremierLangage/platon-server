from django.apps import AppConfig


class PlSandboxConfig(AppConfig):
    name = 'pl_sandbox'


    def ready(self):
        from . import receivers  # keep to receive signals
