import logging

from rest_framework import mixins, viewsets
from rest_framework.serializers import ValidationError
from rest_framework.settings import api_settings
from vng_api_common.permissions import AuthScopesRequired
from vng_api_common.viewsets import CheckQueryParamsMixin

from kcc.datamodel.models import ContactMoment, Klant, ObjectContactMoment
from kcc.datamodel.models.core import ObjectVerzoek, Verzoek

from .filters import ObjectContactMomentFilter, ObjectVerzoekFilter
from .scopes import (
    SCOPE_KLANTEN_AANMAKEN,
    SCOPE_KLANTEN_ALLES_LEZEN,
    SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    SCOPE_KLANTEN_BIJWERKEN,
)
from .serializers import (
    ContactMomentSerializer,
    KlantSerializer,
    ObjectContactMomentSerializer,
    ObjectVerzoekSerializer,
    VerzoekSerializer,
)
from .validators import (
    ObjectContactMomentDestroyValidator,
    ObjectVerzoekDestroyValidator,
)

logger = logging.getLogger(__name__)


class KlantViewSet(viewsets.ModelViewSet):
    """
    Opvragen en bewerken van KLANTen.

    Een KLANT is een eenvoudige weergave van een NATUURLIJK PERSOON of
    VESTIGING waarbij het gaat om niet geverifieerde gegevens. Om deze reden
    zijn ook alle attributen optioneel.

    Indien de KLANT geverifieerd is mag een relatie gelegd worden met een
    NATUURLIJK PERSOON of VESTIGING  middels het attribuut `subject` of, indien
    er geen API beschikbaar is voor deze objecten, middels
    `subjectIdentificatie`.

    create:
    Maak een KLANT aan.

    Maak een KLANT aan.

    list:
    Alle KLANTen opvragen.

    Alle KLANTen opvragen.

    retrieve:
    Een specifiek KLANT opvragen.

    Een specifiek KLANT opvragen.

    update:
    Werk een KLANT in zijn geheel bij.

    Werk een KLANT in zijn geheel bij.

    partial_update:
    Werk een KLANT deels bij.

    Werk een KLANT deels bij.

    destroy:
    Verwijder een KLANT.

    Verwijder een KLANT.
    """

    queryset = Klant.objects.all()
    serializer_class = KlantSerializer
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    required_scopes = {
        "list": SCOPE_KLANTEN_ALLES_LEZEN,
        "retrieve": SCOPE_KLANTEN_ALLES_LEZEN,
        "create": SCOPE_KLANTEN_AANMAKEN,
        "update": SCOPE_KLANTEN_BIJWERKEN,
        "partial_update": SCOPE_KLANTEN_BIJWERKEN,
        "destroy": SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    }


class ContactMomentViewSet(viewsets.ModelViewSet):
    """
    Opvragen en bewerken van CONTACTMOMENTen.

    create:
    Maak een CONTACTMOMENT aan.

    Maak een CONTACTMOMENT aan.

    list:
    Alle CONTACTMOMENTen opvragen.

    Alle CONTACTMOMENTen opvragen.

    retrieve:
    Een specifiek CONTACTMOMENT opvragen.

    Een specifiek CONTACTMOMENT opvragen.

    update:
    Werk een CONTACTMOMENT in zijn geheel bij.

    Werk een CONTACTMOMENT in zijn geheel bij.

    partial_update:
    Werk een CONTACTMOMENT deels bij.

    Werk een CONTACTMOMENT deels bij.

    destroy:
    Verwijder een CONTACTMOMENT.

    Verwijder een CONTACTMOMENT.
    """

    queryset = ContactMoment.objects.all()
    serializer_class = ContactMomentSerializer
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    required_scopes = {
        "list": SCOPE_KLANTEN_ALLES_LEZEN,
        "retrieve": SCOPE_KLANTEN_ALLES_LEZEN,
        "create": SCOPE_KLANTEN_AANMAKEN,
        "update": SCOPE_KLANTEN_BIJWERKEN,
        "partial_update": SCOPE_KLANTEN_BIJWERKEN,
        "destroy": SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    }


class VerzoekViewSet(viewsets.ModelViewSet):
    """
    Opvragen en bewerken van VERZOEKen.

    create:
    Maak een VERZOEK aan.

    Maak een VERZOEK aan.

    list:
    Alle VERZOEKen opvragen.

    Alle VERZOEKen opvragen.

    retrieve:
    Een specifiek VERZOEK opvragen.

    Een specifiek VERZOEK opvragen.

    update:
    Werk een VERZOEK in zijn geheel bij.

    Werk een VERZOEK in zijn geheel bij.

    partial_update:
    Werk een VERZOEK deels bij.

    Werk een VERZOEK deels bij.

    destroy:
    Verwijder een VERZOEK.

    Verwijder een VERZOEK.
    """

    queryset = Verzoek.objects.all()
    serializer_class = VerzoekSerializer
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    required_scopes = {
        "list": SCOPE_KLANTEN_ALLES_LEZEN,
        "retrieve": SCOPE_KLANTEN_ALLES_LEZEN,
        "create": SCOPE_KLANTEN_AANMAKEN,
        "update": SCOPE_KLANTEN_BIJWERKEN,
        "partial_update": SCOPE_KLANTEN_BIJWERKEN,
        "destroy": SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    }


class ObjectContactMomentViewSet(
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en verwijderen van OBJECT-CONTACTMOMENT relaties.

    Het betreft een relatie tussen een willekeurig OBJECT, bijvoorbeeld een
    ZAAK in de Zaken API, en een CONTACTMOMENT.

    create:
    Maak een OBJECT-CONTACTMOMENT relatie aan.

    Maak een OBJECT-CONTACTMOMENT relatie aan.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.

    list:
    Alle OBJECT-CONTACTMOMENT relaties opvragen.

    Alle OBJECT-CONTACTMOMENT relaties opvragen.

    retrieve:
    Een specifiek OBJECT-CONTACTMOMENT relatie opvragen.

    Een specifiek OBJECT-CONTACTMOMENT relatie opvragen.

    destroy:
    Verwijder een OBJECT-CONTACTMOMENT relatie.

    Verwijder een OBJECT-CONTACTMOMENT relatie.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.
    """

    queryset = ObjectContactMoment.objects.all()
    serializer_class = ObjectContactMomentSerializer
    filterset_class = ObjectContactMomentFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    required_scopes = {
        "list": SCOPE_KLANTEN_ALLES_LEZEN,
        "retrieve": SCOPE_KLANTEN_ALLES_LEZEN,
        "create": SCOPE_KLANTEN_AANMAKEN,
        "destroy": SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    }

    def perform_destroy(self, instance):
        # destroy is only allowed if the remote relation does no longer exist, so check for that
        validator = ObjectContactMomentDestroyValidator()

        try:
            validator(instance)
        except ValidationError as exc:
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: exc}, code=exc.detail[0].code
            )
        else:
            super().perform_destroy(instance)


class ObjectVerzoekViewSet(
    CheckQueryParamsMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.ReadOnlyModelViewSet,
):
    """
    Opvragen en verwijderen van OBJECT-VERZOEK relaties.

    Het betreft een relatie tussen een willekeurig OBJECT, bijvoorbeeld een
    ZAAK in de Zaken API, en een VERZOEK.

    create:
    Maak een OBJECT-VERZOEK relatie aan.

    Maak een OBJECT-VERZOEK relatie aan.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.

    list:
    Alle OBJECT-VERZOEK relaties opvragen.

    Alle OBJECT-VERZOEK relaties opvragen.

    retrieve:
    Een specifiek OBJECT-VERZOEK relatie opvragen.

    Een specifiek OBJECT-VERZOEK relatie opvragen.

    destroy:
    Verwijder een OBJECT-VERZOEK relatie.

    Verwijder een OBJECT-VERZOEK relatie.

    **LET OP: Dit endpoint hoor je als consumer niet zelf aan te spreken.**

    Andere API's, zoals de Zaken API, gebruiken dit
    endpoint bij het synchroniseren van relaties.
    """

    queryset = ObjectVerzoek.objects.all()
    serializer_class = ObjectVerzoekSerializer
    filterset_class = ObjectVerzoekFilter
    lookup_field = "uuid"
    permission_classes = (AuthScopesRequired,)
    required_scopes = {
        "list": SCOPE_KLANTEN_ALLES_LEZEN,
        "retrieve": SCOPE_KLANTEN_ALLES_LEZEN,
        "create": SCOPE_KLANTEN_AANMAKEN,
        "destroy": SCOPE_KLANTEN_ALLES_VERWIJDEREN,
    }

    def perform_destroy(self, instance):
        # destroy is only allowed if the remote relation does no longer exist, so check for that
        validator = ObjectVerzoekDestroyValidator()

        try:
            validator(instance)
        except ValidationError as exc:
            raise ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: exc}, code=exc.detail[0].code
            )
        else:
            super().perform_destroy(instance)
