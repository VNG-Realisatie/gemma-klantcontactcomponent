from django.utils.translation import ugettext_lazy as _

from django_filters import filters
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from kic.datamodel.constants import KlantContactMomentRol
from kic.datamodel.models import (
    KlantContactMoment,
    ObjectContactMoment,
    VerzoekContactMoment,
    VerzoekInformatieObject,
    VerzoekProduct,
)
from kic.datamodel.models.core import ObjectVerzoek


class ObjectContactMomentFilter(FilterSet):
    class Meta:
        model = ObjectContactMoment
        fields = ("object", "contactmoment")


class KlantContactMomentFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters["rol"].extra.update({"choices": KlantContactMomentRol.choices})

    class Meta:
        model = KlantContactMoment
        fields = ("contactmoment", "klant", "rol")


class ObjectVerzoekFilter(FilterSet):
    class Meta:
        model = ObjectVerzoek
        fields = ("object", "verzoek")


class VerzoekInformatieObjectFilter(FilterSet):
    class Meta:
        model = VerzoekInformatieObject
        fields = ("verzoek", "informatieobject")


class VerzoekContactMomentFilter(FilterSet):
    class Meta:
        model = VerzoekContactMoment
        fields = ("verzoek", "contactmoment")


class VerzoekProductFilter(FilterSet):
    product_identificatie__code = filters.CharFilter(
        field_name="product_code",
        help_text=get_help_text("datamodel.VerzoekProduct", "product_code"),
    )

    class Meta:
        model = VerzoekProduct
        fields = ("verzoek", "product", "product_identificatie__code")
