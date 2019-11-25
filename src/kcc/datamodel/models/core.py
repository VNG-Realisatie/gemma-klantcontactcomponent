import uuid

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from vng_api_common.models import APIMixin

from ..constants import InitiatiefNemer, KlantType, ObjectTypes

__all__ = ["Klant", "ContactMoment", "ObjectContactMoment", "Verzoek", "ObjectVerzoek"]


class Klant(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    voornaam = models.CharField(
        max_length=200,
        blank=True,
        help_text="De voornaam, voorletters of roepnaam van de klant.",
    )
    achternaam = models.CharField(
        max_length=200, blank=True, help_text="De achternaam van de klant."
    )
    adres = models.CharField(
        max_length=1000, blank=True, help_text="Het adres van de klant."
    )
    telefoonnummer = models.CharField(
        max_length=20,
        blank=True,
        help_text="Het mobiele of vaste telefoonnummer van de klant.",
    )
    emailadres = models.EmailField(
        blank=True, help_text="Het e-mail adres van de klant."
    )
    subject = models.URLField(
        help_text="URL-referentie naar een subject", max_length=1000, blank=True
    )
    subject_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=KlantType.choices,
        help_text="Type van de `subject`.",
    )

    class Meta:
        verbose_name = "klant"
        verbose_name_plural = "klanten"

    @property
    def subject_identificatie(self):
        if hasattr(self, self.subject_type):
            return getattr(self, self.subject_type)
        return None


class KlantInteractie(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    klant = models.ForeignKey(
        Klant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_(
            "URL-referentie naar een KLANT (in de Contactmomenten API) indien het contactmoment niet anoniem is."
        ),
    )
    datumtijd = models.DateTimeField(
        default=timezone.now,
        help_text=_("De datum en het tijdstip waarop het CONTACTMOMENT begint"),
    )
    tekst = models.TextField(
        blank=True,
        help_text=_(
            "Een toelichting die inhoudelijk het contact met de klant beschrijft."
        ),
    )

    class Meta:
        abstract = True


class ContactMoment(APIMixin, KlantInteractie):
    kanaal = models.CharField(
        blank=True,
        max_length=50,
        help_text=_("Het communicatiekanaal waarlangs het CONTACTMOMENT gevoerd wordt"),
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


class Verzoek(APIMixin, KlantInteractie):
    """
    Verzoek is een speciaal contactmoment.
    """

    class Meta:
        verbose_name = "verzoek"
        verbose_name_plural = "verzoeken"


class ObjectKlantInteractie(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
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
        abstract = True


class ObjectContactMoment(APIMixin, ObjectKlantInteractie):
    """
    Modelleer een CONTACTMOMENT horend bij een OBJECT.
    """

    contactmoment = models.ForeignKey(
        "datamodel.ContactMoment",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het CONTACTMOMENT.",
    )

    class Meta:
        verbose_name = "object-contactmoment"
        verbose_name_plural = "object-contactmomenten"
        unique_together = ("contactmoment", "object")


class ObjectVerzoek(APIMixin, ObjectKlantInteractie):
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )

    class Meta:
        verbose_name = "object-verzoek"
        verbose_name_plural = "object-verzoeken"
        unique_together = ("verzoek", "object")
