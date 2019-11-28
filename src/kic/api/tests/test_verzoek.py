from datetime import datetime

from django.utils.timezone import make_aware

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from kic.datamodel.models import Verzoek
from kic.datamodel.tests.factories import KlantFactory, VerzoekFactory


class VerzoekTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_verzoeken(self):
        list_url = reverse(Verzoek)
        VerzoekFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_read_verzoek(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        verzoek = VerzoekFactory.create(
            klant=klant, datumtijd=make_aware(datetime(2019, 1, 1)),
        )
        detail_url = reverse(verzoek)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "klant": f"http://testserver{klant_url}",
                "datumtijd": "2019-01-01T00:00:00Z",
                "tekst": verzoek.tekst,
            },
        )

    def test_create_verzoek(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        list_url = reverse(Verzoek)
        data = {
            "klant": klant_url,
            "tekst": "some text",
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        verzoek = Verzoek.objects.get()

        self.assertEqual(verzoek.klant, klant)
        self.assertEqual(verzoek.tekst, "some text")

    def test_update_verzoek(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        verzoek = VerzoekFactory.create()
        detail_url = reverse(verzoek)

        response = self.client.patch(detail_url, {"klant": klant_url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        verzoek.refresh_from_db()

        self.assertEqual(verzoek.klant, klant)

    def test_destroy_verzoek(self):
        verzoek = VerzoekFactory.create()
        detail_url = reverse(verzoek)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Verzoek.objects.count(), 0)
