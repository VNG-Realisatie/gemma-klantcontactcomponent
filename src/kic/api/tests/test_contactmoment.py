from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from kic.datamodel.constants import InitiatiefNemer
from kic.datamodel.models import ContactMoment
from kic.datamodel.tests.factories import (
    ContactMomentFactory,
    KlantFactory,
    MedewerkerFactory,
)


class ContactMomentTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_contactmomenten(self):
        list_url = reverse(ContactMoment)
        ContactMomentFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_read_contactmoment(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        contactmoment = ContactMomentFactory.create(
            klant=klant,
            datumtijd=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
        )
        detail_url = reverse(contactmoment)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "klant": f"http://testserver{klant_url}",
                "datumtijd": "2019-01-01T00:00:00Z",
                "kanaal": contactmoment.kanaal,
                "tekst": contactmoment.tekst,
                "onderwerpLinks": [],
                "initiatiefnemer": InitiatiefNemer.gemeente,
                "medewerker": contactmoment.medewerker,
                "medewerkerIdentificatie": None,
            },
        )

    def test_read_contactmoment_with_medewerker(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        contactmoment = ContactMomentFactory.create(
            klant=klant,
            datumtijd=make_aware(datetime(2019, 1, 1)),
            initiatiefnemer=InitiatiefNemer.gemeente,
            medewerker="",
        )
        medewerker = MedewerkerFactory.create(contactmoment=contactmoment)
        detail_url = reverse(contactmoment)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "klant": f"http://testserver{klant_url}",
                "datumtijd": "2019-01-01T00:00:00Z",
                "kanaal": contactmoment.kanaal,
                "tekst": contactmoment.tekst,
                "onderwerpLinks": [],
                "initiatiefnemer": InitiatiefNemer.gemeente,
                "medewerker": "",
                "medewerkerIdentificatie": {
                    "identificatie": medewerker.identificatie,
                    "achternaam": medewerker.achternaam,
                    "voorletters": medewerker.voorletters,
                    "voorvoegselAchternaam": medewerker.voorvoegsel_achternaam,
                },
            },
        )

    def test_create_contactmoment(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        list_url = reverse(ContactMoment)
        data = {
            "klant": klant_url,
            "kanaal": "telephone",
            "tekst": "some text",
            "onderwerpLinks": [],
            "initiatiefnemer": InitiatiefNemer.gemeente,
            "medewerker": "http://example.com/medewerker/1",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contactmoment = ContactMoment.objects.get()

        self.assertEqual(contactmoment.klant, klant)
        self.assertEqual(contactmoment.kanaal, "telephone")
        self.assertEqual(contactmoment.tekst, "some text")
        self.assertEqual(contactmoment.initiatiefnemer, InitiatiefNemer.gemeente)
        self.assertEqual(contactmoment.medewerker, "http://example.com/medewerker/1")

    def test_create_contactmoment_with_medewerker(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        list_url = reverse(ContactMoment)
        data = {
            "klant": klant_url,
            "kanaal": "telephone",
            "tekst": "some text",
            "onderwerpLinks": [],
            "initiatiefnemer": InitiatiefNemer.gemeente,
            "medewerkerIdentificatie": {
                "identificatie": "12345",
                "achternaam": "Buurman",
                "voorletters": "B B",
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contactmoment = ContactMoment.objects.get()

        self.assertEqual(contactmoment.klant, klant)
        self.assertEqual(contactmoment.kanaal, "telephone")
        self.assertEqual(contactmoment.tekst, "some text")
        self.assertEqual(contactmoment.initiatiefnemer, InitiatiefNemer.gemeente)

        medewerker = contactmoment.medewerker_identificatie

        self.assertEqual(medewerker.identificatie, "12345")
        self.assertEqual(medewerker.achternaam, "Buurman")
        self.assertEqual(medewerker.voorletters, "B B")

    def test_create_contactmoment_fail_no_medewerker(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        list_url = reverse(ContactMoment)
        data = {
            "klant": klant_url,
            "kanaal": "telephone",
            "tekst": "some text",
            "initiatiefnemer": InitiatiefNemer.gemeente,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error = get_validation_errors(response, "nonFieldErrors")

        self.assertEqual(error["code"], "invalid-medewerker")

    def test_update_contactmoment(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)

        response = self.client.patch(detail_url, {"klant": klant_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contactmoment.refresh_from_db()

        self.assertEqual(contactmoment.klant, klant)

    def test_update_contactmoment_with_medewerker(self):
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)
        data = {
            "medewerker": "",
            "medewerkerIdentificatie": {
                "identificatie": "12345",
                "achternaam": "Buurman",
                "voorletters": "B B",
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contactmoment.refresh_from_db()

        self.assertEqual(contactmoment.medewerker, "")

        medewerker = contactmoment.medewerker_identificatie

        self.assertEqual(medewerker.identificatie, "12345")
        self.assertEqual(medewerker.achternaam, "Buurman")
        self.assertEqual(medewerker.voorletters, "B B")

    def test_destroy_contactmoment(self):
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactMoment.objects.count(), 0)
