import logging

from rest_framework import serializers
from rest_framework.settings import api_settings

from kcc.datamodel.models import ContactMoment, Klant
from kcc.sync.signals import SyncError

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

    def create(self, validated_data):
        zaak = validated_data.pop('zaak', '')
        contactmoment = super().create(validated_data)
        try:
            contactmoment.zaak = zaak
            contactmoment.save()
        except SyncError as sync_error:
            contactmoment.delete()
            raise serializers.ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: sync_error.args[0]},
                code='sync-with-zrc'
            ) from sync_error
        else:
            return contactmoment

