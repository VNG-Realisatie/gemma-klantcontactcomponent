from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "kcc.utils"

    def ready(self):
        from . import checks  # noqa
