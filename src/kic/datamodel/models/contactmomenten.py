import logging
import uuid as _uuid

from django.db import models

logger = logging.getLogger(__name__)


__all__ = ["Medewerker", "VerzoekInformatieObject"]


class Medewerker(models.Model):
    contactmoment = models.OneToOneField(
        "datamodel.ContactMoment",
        on_delete=models.CASCADE,
        related_name="medewerker_identificatie",
    )
    identificatie = models.CharField(
        max_length=24,
        blank=True,
        help_text="Een korte unieke aanduiding van de MEDEWERKER.",
        db_index=True,
    )
    achternaam = models.CharField(
        max_length=200,
        blank=True,
        help_text="De achternaam zoals de MEDEWERKER die in het dagelijkse verkeer gebruikt.",
    )
    voorletters = models.CharField(
        max_length=20,
        blank=True,
        help_text="De verzameling letters die gevormd wordt door de eerste letter van "
        "alle in volgorde voorkomende voornamen.",
    )
    voorvoegsel_achternaam = models.CharField(
        max_length=10,
        blank=True,
        help_text="Dat deel van de geslachtsnaam dat voorkomt in Tabel 36 (GBA), "
        "voorvoegseltabel, en door een spatie van de geslachtsnaam is",
    )

    class Meta:
        verbose_name = "medewerker"


class VerzoekInformatieObject(models.Model):
    uuid = models.UUIDField(
        unique=True, default=_uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    verzoek = models.ForeignKey(
        "datamodel.Verzoek",
        on_delete=models.CASCADE,
        help_text="URL-referentie naar het VERZOEK.",
    )
    informatieobject = models.URLField(
        "informatieobject",
        help_text="URL-referentie naar het INFORMATIEOBJECT (in de Documenten "
        "API) waarin (een deel van) het verzoek beschreven is of "
        "aanvullende informatie biedt bij het VERZOEK.",
        max_length=1000,
    )

    class Meta:
        verbose_name = "verzoekinformatieobject"
        verbose_name_plural = "verzoekinformatieobjecten"
        unique_together = (("verzoek", "informatieobject"),)

    def __str__(self):
        return str(self.uuid)

    # def unique_representation(self):
    #     if not hasattr(self, "_unique_representation"):
    #         io_id = request_object_attribute(
    #             self.informatieobject, "identificatie", "enkelvoudiginformatieobject"
    #         )
    #         self._unique_representation = (
    #             f"({self.verzoek.unique_representation()}) - {io_id}"
    #         )
    #     return self._unique_representation
