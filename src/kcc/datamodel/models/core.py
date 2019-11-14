import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from vng_api_common.models import APIMixin

from ..constants import InitiatiefNemer, KlantType, ObjectTypes

__all__ = ["Klant", "ContactMoment", "ObjectContactMoment"]


class Klant(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    voornaam = models.CharField(max_length=200)
    achternaam = models.CharField(max_length=200)
    adres = models.CharField(max_length=1000, blank=True)
    telefoonnummer = models.CharField(max_length=20, blank=True)
    emailadres = models.EmailField(blank=True)
    betrokkene = models.URLField(
        help_text="URL-referentie naar een betrokkene", max_length=1000, blank=True
    )
    betrokkene_type = models.CharField(
        max_length=100, choices=KlantType.choices, help_text="Type van de `betrokkene`."
    )

    class Meta:
        verbose_name = "klant"
        verbose_name_plural = "klanten"

    @property
    def betrokkene_identificatie(self):
        if hasattr(self, self.betrokkene_type):
            return getattr(self, self.betrokkene_type)
        return None


class ContactMoment(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    klant = models.ForeignKey(
        Klant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_("URL-referentie naar een KLANT (in de KCC API)"),
    )
    datumtijd = models.DateTimeField(
        default=timezone.now,
        help_text=_("De datum en het tijdstip waarop het CONTACTMOMENT begint"),
    )
    kanaal = models.CharField(
        blank=True,
        max_length=50,
        help_text=_("Het communicatiekanaal waarlangs het CONTACTMOMENT gevoerd wordt"),
    )
    tekst = models.TextField(
        blank=True,
        help_text=_(
            "Een toelichting die inhoudelijk het contact met de klant beschrijft."
        ),
    )
    initiatiefnemer = models.CharField(
        max_length=20,
        blank=True,
        choices=InitiatiefNemer.choices,
        help_text=_("De partij die het contact heeft geïnitieerd."),
    )
    medewerker = models.URLField(
        help_text="URL-referentie naar een medewerker", max_length=1000, blank=True
    )

    class Meta:
        verbose_name = "contactmoment"
        verbose_name_plural = "contactmomenten"


class ObjectContactMoment(APIMixin, models.Model):
    """
    Modelleer een CONTACTMOMENT horend bij een OBJECT.
    """

    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    contactmoment = models.ForeignKey(
        ContactMoment,
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het CONTACTMOMENT.",
    )
    object = models.URLField(
        help_text="URL-referentie naar het gerelateerde OBJECT (in een andere API)."
    )
    object_type = models.CharField(
        "objecttype",
        max_length=100,
        choices=ObjectTypes.choices,
        help_text="Het type van het gerelateerde OBJECT.",
    )

    class Meta:
        verbose_name = "object-contactmoment"
        verbose_name_plural = "object-contactmomenten"
        unique_together = ("contactmoment", "object")
