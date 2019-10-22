from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from kcc.datamodel.constants import KlantType
from kcc.datamodel.models import Klant
from kcc.datamodel.tests.factories import (
    AdresFactory,
    KlantFactory,
    NatuurlijkPersoonFactory,
    SubVerblijfBuitenlandFactory,
    VestigingFactory,
)

BETROKKENE = "http://example.com/betrokkene/1"


class KlantTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_klanten(self):
        list_url = reverse(Klant)
        KlantFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_read_klant_url(self):
        klant = KlantFactory.create(
            betrokkene=BETROKKENE, betrokkene_type=KlantType.natuurlijk_persoon
        )
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "voornaam": klant.voornaam,
                "achternaam": klant.achternaam,
                "adres": klant.adres,
                "emailadres": klant.emailadres,
                "telefonnummer": klant.telefonnummer,
                "betrokkene": BETROKKENE,
                "betrokkeneType": KlantType.natuurlijk_persoon,
                "betrokkeneIdentificatie": None,
            },
        )

    def test_read_klant_natuurlijkpersoon(self):
        klant = KlantFactory.create(
            betrokkene=BETROKKENE, betrokkene_type=KlantType.natuurlijk_persoon
        )
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = AdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "voornaam": klant.voornaam,
                "achternaam": klant.achternaam,
                "adres": klant.adres,
                "telefonnummer": klant.telefonnummer,
                "emailadres": klant.emailadres,
                "betrokkene": BETROKKENE,
                "betrokkeneType": KlantType.natuurlijk_persoon,
                "betrokkeneIdentificatie": {
                    "inpBsn": natuurlijkpersoon.inp_bsn,
                    "anpIdentificatie": natuurlijkpersoon.anp_identificatie,
                    "inpANummer": natuurlijkpersoon.inp_a_nummer,
                    "geslachtsnaam": natuurlijkpersoon.geslachtsnaam,
                    "voorvoegselGeslachtsnaam": natuurlijkpersoon.voorvoegsel_geslachtsnaam,
                    "voorletters": natuurlijkpersoon.voorletters,
                    "voornamen": natuurlijkpersoon.voornamen,
                    "geslachtsaanduiding": natuurlijkpersoon.geslachtsaanduiding,
                    "geboortedatum": natuurlijkpersoon.geboortedatum,
                    "verblijfsadres": {
                        "aoaIdentificatie": adres.aoa_identificatie,
                        "wplWoonplaatsNaam": adres.wpl_woonplaats_naam,
                        "gorOpenbareRuimteNaam": adres.gor_openbare_ruimte_naam,
                        "aoaPostcode": adres.aoa_postcode,
                        "aoaHuisnummer": adres.aoa_huisnummer,
                        "aoaHuisletter": adres.aoa_huisletter,
                        "aoaHuisnummertoevoeging": adres.aoa_huisnummertoevoeging,
                        "inpLocatiebeschrijving": adres.inp_locatiebeschrijving,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_read_klant_vestiging(self):
        klant = KlantFactory.create(
            betrokkene=BETROKKENE, betrokkene_type=KlantType.vestiging
        )
        vestiging = VestigingFactory.create(klant=klant)
        adres = AdresFactory.create(vestiging=vestiging)
        buitenland = SubVerblijfBuitenlandFactory.create(vestiging=vestiging)
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "voornaam": klant.voornaam,
                "achternaam": klant.achternaam,
                "adres": klant.adres,
                "telefonnummer": klant.telefonnummer,
                "emailadres": klant.emailadres,
                "betrokkene": BETROKKENE,
                "betrokkeneType": KlantType.vestiging,
                "betrokkeneIdentificatie": {
                    "vestigingsNummer": vestiging.vestigings_nummer,
                    "handelsnaam": vestiging.handelsnaam,
                    "verblijfsadres": {
                        "aoaIdentificatie": adres.aoa_identificatie,
                        "wplWoonplaatsNaam": adres.wpl_woonplaats_naam,
                        "gorOpenbareRuimteNaam": adres.gor_openbare_ruimte_naam,
                        "aoaPostcode": adres.aoa_postcode,
                        "aoaHuisnummer": adres.aoa_huisnummer,
                        "aoaHuisletter": adres.aoa_huisletter,
                        "aoaHuisnummertoevoeging": adres.aoa_huisnummertoevoeging,
                        "inpLocatiebeschrijving": adres.inp_locatiebeschrijving,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_create_klant_url(self):
        list_url = reverse(Klant)
        data = {
            "voornaam": "Xavier",
            "achternaam": "Jackson",
            "emailadres": "test@gmail.com",
            "betrokkeneType": KlantType.natuurlijk_persoon,
            "betrokkene": BETROKKENE,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.voornaam, "Xavier")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "test@gmail.com")
        self.assertEqual(klant.betrokkene, BETROKKENE)

    def test_create_klant_natuurlijkpersoon(self):
        list_url = reverse(Klant)
        data = {
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "betrokkeneType": KlantType.natuurlijk_persoon,
            "betrokkeneIdentificatie": {
                "anpIdentificatie": "123",
                "geslachtsnaam": "Jackson2",
                "voornamen": "Samuel2",
                "geboortedatum": "1962-06-28",
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "East Meaganchester",
                    "gorOpenbareRuimteNaam": "New Amsterdam",
                    "aoaHuisnummer": 21,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.betrokkene, "")
        self.assertEqual(klant.betrokkene_type, KlantType.natuurlijk_persoon)

        natuurlijkpersoon = klant.natuurlijk_persoon

        self.assertEqual(natuurlijkpersoon.anp_identificatie, "123")
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "Jackson2")
        self.assertEqual(natuurlijkpersoon.voornamen, "Samuel2")
        self.assertEqual(natuurlijkpersoon.geboortedatum, "1962-06-28")

        adres = natuurlijkpersoon.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.wpl_woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.aoa_huisnummer, 21)

        buitenland = natuurlijkpersoon.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_create_klant_vestiging(self):
        list_url = reverse(Klant)
        data = {
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "betrokkeneType": KlantType.vestiging,
            "betrokkeneIdentificatie": {
                "vestigingsNummer": "123",
                "handelsnaam": ["WB"],
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "East Meaganchester",
                    "gorOpenbareRuimteNaam": "New Amsterdam",
                    "aoaHuisnummer": 21,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.betrokkene, "")
        self.assertEqual(klant.betrokkene_type, KlantType.vestiging)

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.wpl_woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.aoa_huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_update_klant_url(self):
        klant = KlantFactory.create(betrokkene=BETROKKENE, voornaam="old name")
        detail_url = reverse(klant)

        response = self.client.patch(detail_url, {"voornaam": "new name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.voornaam, "new name")

    def test_update_klant_naturlijkpersoon(self):
        klant = KlantFactory.create(
            betrokkene_type=KlantType.natuurlijk_persoon, betrokkene=BETROKKENE
        )
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = AdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)

        data = {
            "voornaam": "New name",
            "betrokkene": "",
            "betrokkeneIdentificatie": {
                "geslachtsnaam": "New name2",
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "New place",
                    "gorOpenbareRuimteNaam": "New place2",
                    "aoaHuisnummer": 1,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "XXXX",
                    "lndLandnaam": "New land",
                },
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()
        self.assertEqual(klant.voornaam, "New name")
        self.assertEqual(klant.betrokkene, "")

        natuurlijkpersoon.refresh_from_db()
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "New name2")

        adres.refresh_from_db()
        self.assertEqual(adres.wpl_woonplaats_naam, "New place")

        buitenland.refresh_from_db()
        self.assertEqual(buitenland.lnd_landnaam, "New land")

    def test_update_klant_vestiging(self):
        klant = KlantFactory.create(betrokkene_type=KlantType.vestiging)
        detail_url = reverse(klant)

        response = self.client.patch(
            detail_url,
            {
                "betrokkene": "",
                "betrokkeneIdentificatie": {
                    "vestigingsNummer": "123",
                    "handelsnaam": ["WB"],
                    "verblijfsadres": {
                        "aoaIdentificatie": "1234",
                        "wplWoonplaatsNaam": "East Meaganchester",
                        "gorOpenbareRuimteNaam": "New Amsterdam",
                        "aoaHuisnummer": 21,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": "ABCD",
                        "lndLandnaam": "Hollywood",
                    },
                },
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.betrokkene, "")

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.wpl_woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.aoa_huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_update_klant_betrokkene_type_fail(self):
        klant = KlantFactory.create(
            betrokkene=BETROKKENE, betrokkene_type=KlantType.natuurlijk_persoon
        )
        detail_url = reverse(klant)

        response = self.client.patch(
            detail_url, {"betrokkeneType": KlantType.vestiging}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        validation_error = get_validation_errors(response, "betrokkeneType")
        self.assertEqual(validation_error["code"], "wijzigen-niet-toegelaten")

    def test_destroy_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Klant.objects.count(), 0)
