from django.utils.translation import ugettext_lazy as _

from django_filters import filters
from vng_api_common.filters import URLModelChoiceFilter
from vng_api_common.filtersets import FilterSet
from vng_api_common.utils import get_help_text

from kic.datamodel.models import (
    ContactMoment,
    ObjectContactMoment,
    VerzoekContactMoment,
    VerzoekInformatieObject,
    VerzoekProduct,
)
from kic.datamodel.models.core import ObjectVerzoek


class ContactMomentFilter(FilterSet):
    class Meta:
        model = ContactMoment
        fields = ("vorig_contactmoment", "volgend_contactmoment")

    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        # Needed because `volgend_contactmoment` is a reverse OneToOne rel
        if f.name == "volgend_contactmoment":
            filter = URLModelChoiceFilter()
            filter.field_name = "volgend_contactmoment"
            filter.extra["help_text"] = _(
                "URL-referentie naar het volgende CONTACTMOMENT."
            )
            filter.queryset = ContactMoment.objects.all()
        else:
            filter = super().filter_for_field(f, name, lookup_expr)
        return filter


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
