import logging

from rest_framework import serializers

from kcc.datamodel.models import ContactMoment, Klant

logger = logging.getLogger(__name__)


class KlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Klant
        fields = (
            "url",
            "voornaam",
            "achternaam",
            "adres",
            "telefonnummer",
            "emailadres",
        )
        extra_kwargs = {"url": {"lookup_field": "uuid"}}


class ContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContactMoment
        fields = (
            "url",
            "klant",
            "zaak",
            "datumtijd",
            "kanaal",
            "tekst",
            "initiatiefnemer",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "klant": {"lookup_field": "uuid"},
        }
