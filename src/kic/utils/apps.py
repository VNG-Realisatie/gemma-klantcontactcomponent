from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "kic.utils"

    def ready(self):
        from . import checks  # noqa
