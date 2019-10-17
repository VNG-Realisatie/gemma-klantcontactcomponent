from django.contrib import admin

from .models import Klant, ContactMoment


@admin.register(Klant)
class KlantAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactMoment)
class ContactMomentAdmin(admin.ModelAdmin):
    list_display = ['klant']
