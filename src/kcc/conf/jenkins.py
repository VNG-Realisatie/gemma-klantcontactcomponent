from .base import *  # noqa

#
# Standard Django settings.
#

DEBUG = False

ADMINS = ()

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "drc_sync": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/stable/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

LOGGING["loggers"].update(
    {"django": {"handlers": ["django"], "level": "WARNING", "propagate": True}}
)

#
# Custom settings
#

# Show active environment in admin.
ENVIRONMENT = "jenkins"

#
# Jenkins settings
#
INSTALLED_APPS += ["kcc.tests", "django_jenkins"]
PROJECT_APPS = [app for app in INSTALLED_APPS if app.startswith("kcc.")]

JENKINS_TASKS = ("django_jenkins.tasks.run_pylint", "django_jenkins.tasks.run_pep8")
