import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_better_admin_arrayfield.models.fields import ArrayField
from vng_api_common.fields import RSINField
from vng_api_common.models import APIMixin
from vng_api_common.utils import generate_unique_identification
from vng_api_common.validators import alphanumeric_excluding_diacritic

from ..constants import InitiatiefNemer, KlantType, ObjectTypes, VerzoekStatus

__all__ = [
    "Klant",
    "ContactMoment",
    "ObjectContactMoment",
    "Verzoek",
    "ObjectVerzoek",
    "VerzoekProduct",
]


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
    functie = models.CharField(
        max_length=200, blank=True, help_text="De functie van de klant."
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
    bronorganisatie = RSINField(
        help_text="Het RSIN van de Niet-natuurlijk persoon zijnde de "
        "organisatie die de klantinteractie heeft gecreeerd. Dit moet een "
        "geldig RSIN zijn van 9 nummers en voldoen aan "
        "https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef"
    )
    klant = models.ForeignKey(
        Klant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_(
            "URL-referentie naar een KLANT indien de klantinteractie niet anoniem is."
        ),
    )
    interactiedatum = models.DateTimeField(
        default=timezone.now,
        help_text=_(
            "De datum en het tijdstip waarop de klantinteractie heeft plaatsgevonden."
        ),
    )
    tekst = models.TextField(
        blank=True,
        help_text=_(
            "Een toelichting die inhoudelijk de klantinteractie van de klant beschrijft."
        ),
    )
    voorkeurskanaal = models.CharField(
        max_length=50,
        blank=True,
        help_text=_(
            "Het communicatiekanaal dat voor opvolging van de klantinteractie de voorkeur heeft van de KLANT."
        ),
    )
    voorkeurstaal = models.CharField(
        max_length=3,
        blank=True,
        help_text=_(
            "Een ISO 639-2/B taalcode waarin de inhoud van het "
            "INFORMATIEOBJECT is vastgelegd. Voorbeeld: `nld`. Zie: "
            "https://www.iso.org/standard/4767.html"
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
    onderwerp_links = ArrayField(
        models.URLField(
            _("onderwerp link"),
            max_length=1000,
            help_text=_(
                "URL naar een product, webpagina of andere entiteit zodat contactmomenten gegroepeerd kunnen worden."
            ),
        ),
        help_text=_(
            "Eén of meerdere links naar een product, webpagina of andere entiteit "
            "zodat contactmomenten gegroepeerd kunnen worden op onderwerp."
        ),
        blank=True,
        default=list,
    )

    class Meta:
        verbose_name = "contactmoment"
        verbose_name_plural = "contactmomenten"

    def save(self, *args, **kwargs):
        # workaround for https://github.com/gradam/django-better-admin-arrayfield/issues/17
        if self.onderwerp_links is None:
            self.onderwerp_links = []
        super().save(*args, **kwargs)


class Verzoek(APIMixin, KlantInteractie):
    """
    Verzoek is een speciaal contactmoment.
    """

    identificatie = models.CharField(
        max_length=40,
        blank=True,
        help_text="De unieke identificatie van het VERZOEK binnen de "
        "organisatie die verantwoordelijk is voor de behandeling van "
        "het VERZOEK.",
        validators=[alphanumeric_excluding_diacritic],
    )
    externe_identificatie = models.CharField(
        max_length=40,
        blank=True,
        help_text="De identificatie van het VERZOEK buiten de eigen organisatie.",
        validators=[alphanumeric_excluding_diacritic],
    )
    status = models.CharField(
        max_length=20,
        choices=VerzoekStatus,
        help_text="De waarden van de typering van de voortgang van afhandeling van een VERZOEK.",
    )

    class Meta:
        unique_together = ("bronorganisatie", "identificatie")
        verbose_name = "verzoek"
        verbose_name_plural = "verzoeken"

    def save(self, *args, **kwargs):
        if not self.identificatie:
            self.identificatie = generate_unique_identification(self, "interactiedatum")

        super().save(*args, **kwargs)


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


class VerzoekProduct(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )
    product = models.URLField(
        blank=True,
        help_text="URL-referentie naar het PRODUCT (in de Producten en Diensten API).",
    )
    product_code = models.CharField(
        max_length=20, blank=True, help_text="De unieke code van het PRODUCT."
    )

    def clean(self):
        if not self.product and not self.product_code:
            raise ValidationError(
                _("product or productIdentificatie must be provided"),
                code="invalid-product",
            )
