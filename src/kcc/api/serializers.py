import logging

from rest_framework import serializers
from kcc.datamodel.models import Klant, ContactMoment


logger = logging.getLogger(__name__)


class KlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Klant
        fields = ("url",)
        extra_kwarsg = {
            "url": {"lookup_field": "uuid"},
        }


class ContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContactMoment
        fields = ("url", "klant")
        extra_kwarg = {
            "url": {"lookup_field": "uuid"},
            "klant": {"lookup_field": "uuid"},
        }
