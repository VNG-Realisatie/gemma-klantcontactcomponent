from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, reverse

from kic.datamodel.models import VerzoekContactMoment
from kic.datamodel.tests.factories import (
    VerzoekFactory,
    ContactMomentFactory,
    VerzoekContactMomentFactory,
)


class VerzoekContactMomentTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True

    def test_list_verzoekcontactmoment(self):
        list_url = reverse(VerzoekContactMoment)
        VerzoekContactMomentFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_list_filter_verzoekcontactmoment(self):
        list_url = reverse(VerzoekContactMoment)
        vc1 = VerzoekContactMomentFactory.create()
        vc2 = VerzoekContactMomentFactory.create()

        response = self.client.get(
            list_url,
            {"verzoek": f"http://testserver.com{reverse(vc1.verzoek)}"},
            HTTP_HOST="testserver.com",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)

        response = self.client.get(
            list_url,
            {"contactmoment": f"http://testserver.com{reverse(vc2.contactmoment)}"},
            HTTP_HOST="testserver.com",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 1)

    def test_read_verzoekcontactmoment(self):
        verzoekcontactmoment = VerzoekContactMomentFactory.create()
        verzoek_url = reverse(verzoekcontactmoment.verzoek)
        contactmoment_url = reverse(verzoekcontactmoment.contactmoment)

        detail_url = reverse(verzoekcontactmoment)
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "verzoek": f"http://testserver{verzoek_url}",
                "contactmoment": f"http://testserver{contactmoment_url}",
            },
        )

    def test_create_verzoekcontactmoment(self):
        verzoek = VerzoekFactory.create()
        verzoek_url = reverse(verzoek)
        contactmoment = ContactMomentFactory.create()
        contactmoment_url = reverse(contactmoment)

        list_url = reverse(VerzoekContactMoment)
        data = {"verzoek": verzoek_url, "contactmoment": contactmoment_url}

        response = self.client.post(list_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED, response.content
        )

        verzoekcontactmoment = VerzoekContactMoment.objects.get()

        self.assertEqual(verzoekcontactmoment.verzoek, verzoek)
        self.assertEqual(verzoekcontactmoment.contactmoment, contactmoment)

    def test_destroy_verzoekcontactmoment(self):
        verzoekcontactmoment = VerzoekContactMomentFactory.create()
        detail_url = reverse(verzoekcontactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VerzoekContactMoment.objects.count(), 0)
