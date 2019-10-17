import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models
from vng_api_common.models import APIMixin
from phonenumber_field.modelfields import PhoneNumberField


class Klant(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    voornaam = models.CharField(max_length=200)
    achternaam = models.CharField(max_length=200)
    adres = models.CharField(max_length=1000)
    telefonnummer = PhoneNumberField()
    emailadres = models.EmailField()


class ContactMoment(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    klant = models.ForeignKey(
        Klant, on_delete=models.CASCADE, null=True, blank=True
    )
    zaak = models.URLField(
        'zaak', blank=True,  # een besluit kan niet bij een zaak horen (zoals raadsbesluit)
        help_text=_("URL-referentie naar de ZAAK (in de Zaken API)")
    )
    identificatie = models.CharField(
        max_length=14,
        unique=True,
        help_text=_("De unieke aanduiding van een CONTACTMOMENT"),
    )
    datumtijd = models.DateTimeField(
        help_text=_("De datum en het tijdstip waarop het CONTACTMOMENT begint")
    )
    kanaal = models.CharField(
        blank=True,
        max_length=20,
        help_text=_("Het communicatiekanaal waarlangs het CONTACTMOMENT gevoerd wordt"),
    )
    text = models.TextField(
        blank=True,
        help_text=_(
            "Een toelichting die inhoudelijk het contact met de klant beschrijft."
        ),
    )
