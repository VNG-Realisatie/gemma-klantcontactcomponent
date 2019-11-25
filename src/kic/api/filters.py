from vng_api_common.filtersets import FilterSet

from kic.datamodel.models import ObjectContactMoment, VerzoekInformatieObject
from kic.datamodel.models.core import ObjectVerzoek


class ObjectContactMomentFilter(FilterSet):
    class Meta:
        model = ObjectContactMoment
        fields = ("object", "contactmoment")


class ObjectVerzoekFilter(FilterSet):
    class Meta:
        model = ObjectVerzoek
        fields = ("object", "verzoek")


class VerzoekInformatieObjectFilter(FilterSet):
    class Meta:
        model = VerzoekInformatieObject
        fields = ("verzoek", "informatieobject")
