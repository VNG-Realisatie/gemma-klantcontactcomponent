from django.utils.translation import ugettext_lazy as _

from djchoices import ChoiceItem, DjangoChoices


class InitiatiefNemer(DjangoChoices):
    gemeente = ChoiceItem("gemeente", _("gemeente"))
    klant = ChoiceItem("klant", _("klant"))


class GeslachtsAanduiding(DjangoChoices):
    man = ChoiceItem("m", "Man")
    vrouw = ChoiceItem("v", "Vrouw")
    onbekend = ChoiceItem("o", "Onbekend")


class KlantType(DjangoChoices):
    natuurlijk_persoon = ChoiceItem("natuurlijk_persoon", "Natuurlijk persoon")
    vestiging = ChoiceItem("vestiging", "Vestiging")
