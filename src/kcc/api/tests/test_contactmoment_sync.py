from unittest.mock import patch

from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import (
    JWTAuthMixin,
    get_operation_url,
    get_validation_errors,
    reverse,
)
from zds_client.tests.mocks import mock_client

from kcc.datamodel.constants import InitiatiefNemer
from kcc.datamodel.models import ContactMoment
from kcc.datamodel.tests.factories import ContactMomentFactory, KlantFactory
from kcc.sync.signals import SyncError

from .mixins import ContactMomentSyncMixin


class ContactMomentSyncTests(ContactMomentSyncMixin, JWTAuthMixin, APITestCase):

    heeft_alle_autorisaties = True

    def test_create_sync(self):
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        list_url = reverse(ContactMoment)
        data = {
            "klant": klant_url,
            "zaak": "http://www.example.com/zrc/api/v1/zaken/1",
            "kanaal": "telephone",
            "tekst": "some text",
            "initiatiefnemer": InitiatiefNemer.gemeente,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.mocked_sync_create.assert_called_once()
        self.mocked_sync_delete.assert_not_called()

        contactmoment = ContactMoment.objects.get()

        self.mocked_sync_create.assert_called_with(contactmoment)

    def test_create_sync_fails(self):
        self.mocked_sync_create.side_effect = SyncError("Sync failed")
        klant = KlantFactory.create()
        klant_url = reverse(klant)
        list_url = reverse(ContactMoment)
        data = {
            "klant": klant_url,
            "zaak": "http://www.example.com/zrc/api/v1/zaken/1",
            "kanaal": "telephone",
            "tekst": "some text",
            "initiatiefnemer": InitiatiefNemer.gemeente,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )

        error = get_validation_errors(response, "nonFieldErrors")
        self.assertEqual(error["code"], "sync-with-zrc")

        self.assertFalse(ContactMoment.objects.exists())

    def test_delete_sync(self):
        contactmoment = ContactMomentFactory.create(
            _zaakcontactmoment="https://example.com/zrc/zaakcontactmoment/abcd"
        )
        detail_url = reverse(contactmoment)

        response = self.client.delete(detail_url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, response.data
        )

        args = self.mocked_sync_delete.call_args[0]

        #  can't assert args directly because contactmoment object doesn't longer exist
        self.assertEqual(args[0].uuid, contactmoment.uuid)
