from django.contrib import admin

from .models import ContactMoment, Klant


@admin.register(Klant)
class KlantAdmin(admin.ModelAdmin):
    list_display = ["voornaam", "achternaam"]


@admin.register(ContactMoment)
class ContactMomentAdmin(admin.ModelAdmin):
    list_display = ["klant", "zaak", "kanaal"]
