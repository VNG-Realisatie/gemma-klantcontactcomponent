from collections import OrderedDict

from django.conf import settings
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from rest_framework import exceptions, serializers
from vng_api_common.models import APICredential
from vng_api_common.validators import ResourceValidator
from zds_client import ClientError

from kcc.datamodel.models import ObjectContactMoment

from .auth import get_auth
from .utils import get_absolute_url


class ObjectContactMomentDestroyValidator:
    message = _(
        "The canonical remote relation still exists, this relation cannot be deleted."
    )
    code = "remote-relation-exists"

    def __call__(self, objectcontactmoment: ObjectContactMoment):
        object_url = objectcontactmoment.object
        contactmoment_url = get_absolute_url(
            "contactmoment-detail", uuid=objectcontactmoment.contactmoment.uuid
        )

        Client = import_string(settings.ZDS_CLIENT_CLASS)
        client = Client.from_url(object_url)
        client.auth = APICredential.get_auth(object_url)

        resource = f"{objectcontactmoment.object_type}contactmoment"

        try:
            relations = client.list(
                resource,
                query_params={
                    objectcontactmoment.object_type: object_url,
                    "contactmoment": contactmoment_url,
                },
            )
        except ClientError as exc:
            raise serializers.ValidationError(
                exc.args[0], code="relation-lookup-error"
            ) from exc

        if len(relations) >= 1:
            raise serializers.ValidationError(self.message, code=self.code)


class ObjectInformatieObjectCreateValidator:
    """
    Validate that the CONTACTMOMENT is already linked to the OBJECT in the remote component.
    """

    message = _("The contactmoment has no relations to {object}")
    code = "inconsistent-relation"

    def __call__(self, attrs: OrderedDict):
        object_url = attrs["object"]
        object_type = attrs["object_type"]
        contactmoment_url = get_absolute_url(
            "contactmoment-detail", uuid=attrs["contactmoment"].uuid
        )

        # dynamic so that it can be mocked in tests easily
        Client = import_string(settings.ZDS_CLIENT_CLASS)
        client = Client.from_url(object_url)
        client.auth = APICredential.get_auth(object_url)

        resource = f"{object_type}contactmoment"
        oas_schema = settings.ZRC_API_SPEC

        try:
            ResourceValidator(
                object_type.capitalize(),
                oas_schema,
                get_auth=get_auth,
                headers={"Accept-Crs": "EPSG:4326"},
            )(object_url)
        except exceptions.ValidationError as exc:
            raise serializers.ValidationError(
                {"object": exc.detail}, code=ResourceValidator.code
            )

        try:
            relations = client.list(
                resource,
                query_params={
                    object_type: object_url,
                    "contactmoment": contactmoment_url,
                },
            )

        except ClientError as exc:
            raise serializers.ValidationError(
                exc.args[0], code="relation-validation-error"
            ) from exc

        if len(relations) == 0:
            raise serializers.ValidationError(
                self.message.format(object=object_type), code=self.code
            )
