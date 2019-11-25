from django.apps import AppConfig


class SyncConfig(AppConfig):
    name = "kic.sync"

    def ready(self):
        from . import signals  # noqa
