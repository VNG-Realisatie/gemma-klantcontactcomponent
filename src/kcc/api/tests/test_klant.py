from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from kcc.datamodel.models import Klant
from kcc.datamodel.tests.factories import KlantFactory, NatuurlijkPersoonFactory, VestigingFactory, \
    AdresFactory, SubVerblijfBuitenlandFactory
from kcc.datamodel.constants import KlantType

BETROKKENE = 'http://example.com/betrokkene/1'


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
        klant = KlantFactory.create(betrokkene=BETROKKENE, betrokkene_type=KlantType.natuurlijk_persoon)
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
        klant = KlantFactory.create(betrokkene=BETROKKENE, betrokkene_type=KlantType.natuurlijk_persoon)
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = AdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        expected_data = {
                'url': f'http://testserver{detail_url}',
                'voornaam': klant.voornaam,
                'achternaam': klant.achternaam,
                'adres': klant.adres,
                'telefonnummer': klant.telefonnummer,
                'emailadres': klant.emailadres,
                'betrokkene': BETROKKENE,
                'betrokkeneType': KlantType.natuurlijk_persoon,
                'betrokkeneIdentificatie': {
                    'inpBsn': natuurlijkpersoon.inp_bsn,
                    'anpIdentificatie': natuurlijkpersoon.anp_identificatie,
                    'inpANummer': natuurlijkpersoon.inp_a_nummer,
                    'geslachtsnaam': natuurlijkpersoon.geslachtsnaam,
                    'voorvoegselGeslachtsnaam': natuurlijkpersoon.voorvoegsel_geslachtsnaam,
                    'voorletters': natuurlijkpersoon.voorletters,
                    'voornamen': natuurlijkpersoon.voornamen,
                    'geslachtsaanduiding': natuurlijkpersoon.geslachtsaanduiding,
                    'geboortedatum': natuurlijkpersoon.geboortedatum,
                    'verblijfsadres': {
                        'aoaIdentificatie': adres.aoa_identificatie,
                        'wplWoonplaatsNaam': adres.wpl_woonplaats_naam,
                        'gorOpenbareRuimteNaam': adres.gor_openbare_ruimte_naam,
                        'aoaPostcode': adres.aoa_postcode,
                        'aoaHuisnummer': adres.aoa_huisnummer,
                        'aoaHuisletter': adres.aoa_huisletter,
                        'aoaHuisnummertoevoeging': adres.aoa_huisnummertoevoeging,
                        'inpLocatiebeschrijving': adres.inp_locatiebeschrijving,
                    },
                    'subVerblijfBuitenland': {
                        'lndLandcode': buitenland.lnd_landcode,
                        'lndLandnaam': buitenland.lnd_landnaam,
                        'subAdresBuitenland1': buitenland.sub_adres_buitenland_1,
                        'subAdresBuitenland2': buitenland.sub_adres_buitenland_2,
                        'subAdresBuitenland3': buitenland.sub_adres_buitenland_3,
                    }
                }
            }

        self.assertEqual(
            data,
            expected_data
        )

    def test_create_klant(self):
        list_url = reverse(Klant)
        data = {
            "voornaam": "Xavier",
            "achternaam": "Jackson",
            "emailadres": "test@gmail.com",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.voornaam, "Xavier")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "test@gmail.com")

    def test_update_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.patch(detail_url, {"voornaam": "new name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.voornaam, "new name")

    def test_destroy_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Klant.objects.count(), 0)
