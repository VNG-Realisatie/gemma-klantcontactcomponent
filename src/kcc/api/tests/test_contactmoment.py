from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from kcc.datamodel.constants import InitiatiefNemer
from kcc.datamodel.models import ContactMoment
from kcc.datamodel.tests.factories import ContactMomentFactory, KlantFactory


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
                "zaak": contactmoment.zaak,
                "datumtijd": "2019-01-01T00:00:00Z",
                "kanaal": contactmoment.kanaal,
                "text": contactmoment.text,
                "initiatiefnemer": InitiatiefNemer.gemeente,
            },
        )

    def test_create_contactmoment(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        list_url = reverse(ContactMoment)
        data = {
            "klant": klant_url,
            "zaak": "http://www.example.com/zrc/api/v1/zaken/1",
            "kanaal": "telephone",
            "text": "some text",
            "initiatiefnemer": InitiatiefNemer.gemeente,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        contactmoment = ContactMoment.objects.get()

        self.assertEqual(contactmoment.klant, klant)
        self.assertEqual(
            contactmoment.zaak, "http://www.example.com/zrc/api/v1/zaken/1"
        )
        self.assertEqual(contactmoment.kanaal, "telephone")
        self.assertEqual(contactmoment.text, "some text")
        self.assertEqual(contactmoment.initiatiefnemer, InitiatiefNemer.gemeente)

    def test_update_contactmoment(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)

        response = self.client.patch(detail_url, {"klant": klant_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        contactmoment.refresh_from_db()

        self.assertEqual(contactmoment.klant, klant)

    def test_destroy_contactmoment(self):
        contactmoment = ContactMomentFactory.create()
        detail_url = reverse(contactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ContactMoment.objects.count(), 0)
