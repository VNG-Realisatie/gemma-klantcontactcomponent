from vng_api_common.filtersets import FilterSet

from kcc.datamodel.models import ObjectContactMoment
from kcc.datamodel.models.core import ObjectVerzoek


class ObjectContactMomentFilter(FilterSet):
    class Meta:
        model = ObjectContactMoment
        fields = ("object", "contactmoment")


class ObjectVerzoekFilter(FilterSet):
    class Meta:
        model = ObjectVerzoek
        fields = ("object", "verzoek")
