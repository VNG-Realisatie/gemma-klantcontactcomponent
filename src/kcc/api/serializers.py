import logging

from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from vng_api_common.polymorphism import Discriminator, PolymorphicSerializer
from vng_api_common.serializers import add_choice_values_help_text
from vng_api_common.validators import IsImmutableValidator

from kcc.datamodel.constants import GeslachtsAanduiding, KlantType, ObjectTypes
from kcc.datamodel.models import (
    Adres,
    ContactMoment,
    Klant,
    Medewerker,
    NatuurlijkPersoon,
    ObjectContactMoment,
    SubVerblijfBuitenland,
    Vestiging,
)

from .validators import ObjectContactMomentCreateValidator

logger = logging.getLogger(__name__)


# klant models
class SubVerblijfBuitenlandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVerblijfBuitenland
        fields = (
            "lnd_landcode",
            "lnd_landnaam",
            "sub_adres_buitenland_1",
            "sub_adres_buitenland_2",
            "sub_adres_buitenland_3",
        )


class VerblijfsAdresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adres
        fields = (
            "aoa_identificatie",
            "wpl_woonplaats_naam",
            "gor_openbare_ruimte_naam",
            "aoa_postcode",
            "aoa_huisnummer",
            "aoa_huisletter",
            "aoa_huisnummertoevoeging",
            "inp_locatiebeschrijving",
        )


class NatuurlijkPersoonSerializer(serializers.ModelSerializer):
    verblijfsadres = VerblijfsAdresSerializer(required=False, allow_null=True)
    sub_verblijf_buitenland = SubVerblijfBuitenlandSerializer(
        required=False, allow_null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(GeslachtsAanduiding)
        self.fields["geslachtsaanduiding"].help_text += f"\n\n{value_display_mapping}"

    class Meta:
        model = NatuurlijkPersoon
        fields = (
            "inp_bsn",
            "anp_identificatie",
            "inp_a_nummer",
            "geslachtsnaam",
            "voorvoegsel_geslachtsnaam",
            "voorletters",
            "voornamen",
            "geslachtsaanduiding",
            "geboortedatum",
            "verblijfsadres",
            "sub_verblijf_buitenland",
        )

    def create(self, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        natuurlijkpersoon = super().create(validated_data)

        if verblijfsadres_data:
            verblijfsadres_data["natuurlijkpersoon"] = natuurlijkpersoon
            VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            sub_verblijf_buitenland_data["natuurlijkpersoon"] = natuurlijkpersoon
            SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)

        return natuurlijkpersoon

    def update(self, instance, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        natuurlijkpersoon = super().update(instance, validated_data)

        if verblijfsadres_data:
            if hasattr(natuurlijkpersoon, "verblijfsadres"):
                VerblijfsAdresSerializer().update(
                    natuurlijkpersoon.verblijfsadres, verblijfsadres_data
                )
            else:
                verblijfsadres_data["natuurlijkpersoon"] = natuurlijkpersoon
                VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            if hasattr(natuurlijkpersoon, "sub_verblijf_buitenland"):
                SubVerblijfBuitenlandSerializer().update(
                    natuurlijkpersoon.sub_verblijf_buitenland,
                    sub_verblijf_buitenland_data,
                )
            else:
                sub_verblijf_buitenland_data["natuurlijkpersoon"] = natuurlijkpersoon
                SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)

        return natuurlijkpersoon


class VestigingSerializer(serializers.ModelSerializer):
    verblijfsadres = VerblijfsAdresSerializer(required=False, allow_null=True)
    sub_verblijf_buitenland = SubVerblijfBuitenlandSerializer(
        required=False, allow_null=True
    )

    class Meta:
        model = Vestiging
        fields = (
            "vestigings_nummer",
            "handelsnaam",
            "verblijfsadres",
            "sub_verblijf_buitenland",
        )

    def create(self, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        vestiging = super().create(validated_data)

        if verblijfsadres_data:
            verblijfsadres_data["vestiging"] = vestiging
            VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            sub_verblijf_buitenland_data["vestiging"] = vestiging
            SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)
        return vestiging

    def update(self, instance, validated_data):
        verblijfsadres_data = validated_data.pop("verblijfsadres", None)
        sub_verblijf_buitenland_data = validated_data.pop(
            "sub_verblijf_buitenland", None
        )
        vestiging = super().update(instance, validated_data)

        if verblijfsadres_data:
            if hasattr(vestiging, "verblijfsadres"):
                VerblijfsAdresSerializer().update(
                    vestiging.verblijfsadres, verblijfsadres_data
                )
            else:
                verblijfsadres_data["vestiging"] = vestiging
                VerblijfsAdresSerializer().create(verblijfsadres_data)

        if sub_verblijf_buitenland_data:
            if hasattr(vestiging, "sub_verblijf_buitenland"):
                SubVerblijfBuitenlandSerializer().update(
                    vestiging.sub_verblijf_buitenland, sub_verblijf_buitenland_data
                )
            else:
                sub_verblijf_buitenland_data["vestiging"] = vestiging
                SubVerblijfBuitenlandSerializer().create(sub_verblijf_buitenland_data)

        return vestiging


# ContactMoment models
class MedewerkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medewerker
        fields = (
            "identificatie",
            "achternaam",
            "voorletters",
            "voorvoegsel_achternaam",
        )


# main models
class KlantSerializer(PolymorphicSerializer):
    discriminator = Discriminator(
        discriminator_field="subject_type",
        mapping={
            KlantType.natuurlijk_persoon: NatuurlijkPersoonSerializer(),
            KlantType.vestiging: VestigingSerializer(),
        },
        group_field="subject_identificatie",
        same_model=False,
    )

    class Meta:
        model = Klant
        fields = (
            "url",
            "voornaam",
            "achternaam",
            "adres",
            "telefoonnummer",
            "emailadres",
            "subject",
            "subject_type",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "subject": {"required": False},
            "subject_type": {"validators": [IsImmutableValidator()]},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(KlantType)
        self.fields["subject_type"].help_text += f"\n\n{value_display_mapping}"

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)
        subject = validated_attrs.get("subject", None)
        subject_identificatie = validated_attrs.get("subject_identificatie", None)

        if self.instance:
            subject = subject or self.instance.subject
            subject_identificatie = (
                subject_identificatie or self.instance.subject_identificatie
            )

        if not subject and not subject_identificatie:
            raise serializers.ValidationError(
                _("subject or subjectIdentificatie must be provided"),
                code="invalid-subject",
            )

        return validated_attrs

    def to_internal_value(self, data):
        """rewrite method to support update"""
        if self.discriminator.discriminator_field not in data and self.instance:
            data[self.discriminator.discriminator_field] = getattr(
                self.instance, self.discriminator.discriminator_field
            )

        return super().to_internal_value(data)

    @transaction.atomic
    def create(self, validated_data):
        group_data = validated_data.pop("subject_identificatie", None)
        klant = super().create(validated_data)

        if group_data:
            group_serializer = self.discriminator.mapping[
                validated_data["subject_type"]
            ]
            serializer = group_serializer.get_fields()["subject_identificatie"]
            group_data["klant"] = klant
            serializer.create(group_data)

        return klant

    @transaction.atomic
    def update(self, instance, validated_data):
        group_data = validated_data.pop("subject_identificatie", None)
        klant = super().update(instance, validated_data)
        subject_type = validated_data.get("subject_type", klant.subject_type)

        if group_data:
            group_serializer = self.discriminator.mapping[subject_type]
            serializer = group_serializer.get_fields()["subject_identificatie"]
            group_instance = klant.subject_identificatie
            if group_instance:
                serializer.update(group_instance, group_data)
            else:
                group_data["klant"] = klant
                serializer.create(group_data)

        return klant


class ContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    medewerker_identificatie = MedewerkerSerializer(required=False, allow_null=True)

    class Meta:
        model = ContactMoment
        fields = (
            "url",
            "klant",
            "datumtijd",
            "kanaal",
            "tekst",
            "initiatiefnemer",
            "medewerker",
            "medewerker_identificatie",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "klant": {"lookup_field": "uuid"},
        }

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)

        medewerker = validated_attrs.get("medewerker", None)
        medewerker_identificatie = validated_attrs.get("medewerker_identificatie", None)

        if self.instance:
            medewerker = medewerker or self.instance.medewerker
            medewerker_identificatie = medewerker_identificatie or getattr(
                self.instance, "medewerker_identificatie", None
            )

        if not medewerker and not medewerker_identificatie:
            raise serializers.ValidationError(
                _("medewerker or medewerkerIdentificatie must be provided"),
                code="invalid-medewerker",
            )

        return validated_attrs

    def create(self, validated_data):
        medewerker_identificatie_data = validated_data.pop(
            "medewerker_identificatie", None
        )
        contactmoment = super().create(validated_data)

        if medewerker_identificatie_data:
            medewerker_identificatie_data["contactmoment"] = contactmoment
            MedewerkerSerializer().create(medewerker_identificatie_data)

        return contactmoment

    def update(self, instance, validated_data):
        medewerker_identificatie_data = validated_data.pop(
            "medewerker_identificatie", None
        )
        contactmoment = super().update(instance, validated_data)

        if medewerker_identificatie_data:
            if hasattr(contactmoment, "medewerker_identificatie"):
                MedewerkerSerializer().update(
                    contactmoment.medewerker_identificatie,
                    medewerker_identificatie_data,
                )
            else:
                medewerker_identificatie_data["contactmoment"] = contactmoment
                MedewerkerSerializer().create(medewerker_identificatie_data)

        return contactmoment


class ObjectContactMomentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ObjectContactMoment
        fields = ("url", "contactmoment", "object", "object_type")
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "contactmoment": {
                "lookup_field": "uuid",
                "validators": [IsImmutableValidator()],
            },
            "object": {"validators": [IsImmutableValidator()],},
            "object_type": {"validators": [IsImmutableValidator()]},
        }
        validators = [ObjectContactMomentCreateValidator()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(ObjectTypes)
        self.fields["object_type"].help_text += f"\n\n{value_display_mapping}"

        if not hasattr(self, "initial_data"):
            return
