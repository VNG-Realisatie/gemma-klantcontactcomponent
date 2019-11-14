from django.db import models

__all__ = ["Medewerker"]


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
