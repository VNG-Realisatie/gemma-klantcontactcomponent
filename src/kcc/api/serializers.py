import logging

from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from vng_api_common.serializers import add_choice_values_help_text
from vng_api_common.polymorphism import Discriminator, PolymorphicSerializer

from kcc.datamodel.constants import GeslachtsAanduiding, KlantType
from kcc.datamodel.models import (
    Adres,
    ContactMoment,
    Klant,
    NatuurlijkPersoon,
    SubVerblijfBuitenland,
    Vestiging,
)

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


# main models
class KlantSerializer(PolymorphicSerializer):
    discriminator = Discriminator(
        discriminator_field="betrokkene_type",
        mapping={
            KlantType.natuurlijk_persoon: NatuurlijkPersoonSerializer(),
            KlantType.vestiging: VestigingSerializer(),
        },
        group_field="betrokkene_identificatie",
        same_model=False,
    )

    class Meta:
        model = Klant
        fields = (
            "url",
            "voornaam",
            "achternaam",
            "adres",
            "telefonnummer",
            "emailadres",
            "betrokkene",
            "betrokkene_type",
        )
        extra_kwargs = {
            "url": {"lookup_field": "uuid"},
            "betrokkene": {"required": False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        value_display_mapping = add_choice_values_help_text(KlantType)
        self.fields["betrokkene_type"].help_text += f"\n\n{value_display_mapping}"

    def validate(self, attrs):
        validated_attrs = super().validate(attrs)
        betrokkene = validated_attrs.get("betrokkene", None)
        betrokkene_identificatie = validated_attrs.get("betrokkene_identificatie", None)

        if not betrokkene and not betrokkene_identificatie:
            raise serializers.ValidationError(
                _("betrokkene or betrokkeneIdentificatie must be provided"),
                code="invalid-betrokkene",
            )

        return validated_attrs

    @transaction.atomic
    def create(self, validated_data):
        group_data = validated_data.pop("betrokkene_identificatie", None)
        klant = super().create(validated_data)

        if group_data:
            group_serializer = self.discriminator.mapping[
                validated_data["betrokkene_type"]
            ]
            serializer = group_serializer.get_fields()["betrokkene_identificatie"]
            group_data["klant"] = klant
            serializer.create(group_data)

        return klant


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
