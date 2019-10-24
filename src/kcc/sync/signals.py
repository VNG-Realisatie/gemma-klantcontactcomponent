import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse

from vng_api_common.models import APICredential
from zds_client import Client

from kcc.datamodel.models import ContactMoment

logger = logging.getLogger(__name__)


class SyncError(Exception):
    pass


def sync_create_contactmoment(contactmoment: ContactMoment):

    # build the URL of the contactmoment
    path = reverse(
        "contactmoment-detail",
        kwargs={
            "version": settings.REST_FRAMEWORK["DEFAULT_VERSION"],
            "uuid": contactmoment.uuid,
        },
    )
    domain = Site.objects.get_current().domain
    protocol = "https" if settings.IS_HTTPS else "http"
    contactmoment_url = f"{protocol}://{domain}{path}"

    logger.info("Zaak object: %s", contactmoment.zaak)
    logger.info("ContactMoment object: %s", contactmoment_url)

    # figure out which remote resource we need to interact with
    client = Client.from_url(contactmoment.zaak)
    client.auth = APICredential.get_auth(contactmoment.zaak)

    try:
        response = client.create(
            "zaakcontactmoment",
            {"contactmoment": contactmoment_url, "zaak": contactmoment.zaak},
        )
    except Exception as exc:
        logger.error(f"Could not create ZaakContactMoment", exc_info=1)
        raise SyncError(f"Could not create ZaakContactMoment") from exc

    # save ZaakContactMoment url for delete signal
    contactmoment._zaakcontactmoment = response["url"]
    contactmoment.save()


def sync_delete_contactmoment(contactmoment: ContactMoment):
    client = Client.from_url(contactmoment._zaakcontactmoment)
    client.auth = APICredential.get_auth(contactmoment._zaakcontactmoment)
    try:
        client.delete("zaakcontactmoment", url=contactmoment._zaakcontactmoment)
    except Exception as exc:
        logger.error(f"Could not delete ZaakContactMoment", exc_info=1)
        raise SyncError(f"Could not delete ZaakContactMoment") from exc


@receiver([post_save, post_delete], sender=ContactMoment)
def sync_contactmoment(sender, instance: ContactMoment = None, **kwargs):
    signal = kwargs["signal"]
    if signal is post_save and instance.zaak and not instance._zaakcontactmoment:
        sync_create_contactmoment(instance)
    elif signal is post_delete and instance._zaakcontactmoment:
        sync_delete_contactmoment(instance)
