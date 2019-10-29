from vng_api_common.filtersets import FilterSet

from kcc.datamodel.models import ObjectContactMoment


class ObjectContactMomentFilter(FilterSet):
    class Meta:
        model = ObjectContactMoment
        fields = ("object", "contactmoment")
