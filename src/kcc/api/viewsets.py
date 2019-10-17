import logging

from rest_framework import viewsets
from vng_api_common.permissions import BaseAuthRequired

from .serializers import KlantSerializer, ContactMomentSerializer
from kcc.datamodel.models import Klant, ContactMoment

logger = logging.getLogger(__name__)


class KlantViewSet(viewsets.ModelViewSet):
    """
    Opvragen en bewerken van KLANTen.

    create:
    Maak een KLANT aan.

    Maak een KLANT aan.

    list:
    Alle KLANTen opvragen.

    Alle KLANTen opvragen.

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


class ContactMomentViewSet(viewsets.ModelViewSet):
    """
    Opvragen en bewerken van CONTACTMOMENTen.

    create:
    Maak een CONTACTMOMENT aan.

    Maak een CONTACTMOMENT aan.

    list:
    Alle CONTACTMOMENTen opvragen.

    Alle CONTACTMOMENTen opvragen.

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


