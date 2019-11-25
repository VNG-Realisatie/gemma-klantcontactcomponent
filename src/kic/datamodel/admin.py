from django.contrib import admin

from .models import (
    Adres,
    ContactMoment,
    Klant,
    Medewerker,
    NatuurlijkPersoon,
    ObjectContactMoment,
    SubVerblijfBuitenland,
    Vestiging,
)


@admin.register(Klant)
class KlantAdmin(admin.ModelAdmin):
    list_display = ["voornaam", "achternaam"]


@admin.register(ContactMoment)
class ContactMomentAdmin(admin.ModelAdmin):
    list_display = ["klant", "kanaal"]


@admin.register(ObjectContactMoment)
class ObjectContactMomentAdmin(admin.ModelAdmin):
    list_display = ["contactmoment", "object"]


# klant models
@admin.register(NatuurlijkPersoon)
class NatuurlijkPersoonAdmin(admin.ModelAdmin):
    list_display = ["klant", "inp_bsn", "anp_identificatie", "inp_a_nummer"]


@admin.register(Vestiging)
class VestigingAdmin(admin.ModelAdmin):
    list_display = ["klant", "vestigings_nummer"]


@admin.register(SubVerblijfBuitenland)
class SubVerblijfBuitenlandAdmin(admin.ModelAdmin):
    list_display = ["natuurlijkpersoon", "vestiging", "lnd_landcode"]


@admin.register(Adres)
class AdresAdmin(admin.ModelAdmin):
    list_display = ["natuurlijkpersoon", "vestiging", "aoa_identificatie"]


# ContactMoment models
@admin.register(Medewerker)
class MedewerkerAdmin(admin.ModelAdmin):
    list_display = ["contactmoment", "identificatie"]
