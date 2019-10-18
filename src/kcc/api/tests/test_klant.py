from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from kcc.datamodel.models import Klant
from kcc.datamodel.tests.factories import KlantFactory


class KlantTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_klanten(self):
        list_url = reverse(Klant)
        KlantFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_read_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                'url': f'http://testserver{detail_url}',
                'voornaam': klant.voornaam,
                'achternaam': klant.achternaam,
                'adres': klant.adres,
                'emailadres': klant.emailadres,
                'telefonnummer': klant.telefonnummer,
            }
        )

    def test_create_klant(self):
        list_url = reverse(Klant)
        data = {
            'voornaam': 'Xavier',
            'achternaam': 'Jackson',
            'emailadres': 'test@gmail.com'
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.voornaam, 'Xavier')
        self.assertEqual(klant.achternaam, 'Jackson')
        self.assertEqual(klant.emailadres, 'test@gmail.com')

    def test_update_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.patch(detail_url, {'voornaam': "new name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.voornaam, "new name")

    def test_destroy_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Klant.objects.count(), 0)
