import factory.fuzzy

from ..constants import InitiatiefNemer


class KlantFactory(factory.django.DjangoModelFactory):
    voornaam = factory.Faker("first_name")
    achternaam = factory.Faker("last_name")
    adres = factory.Faker("address")
    emailadres = factory.Faker("email")

    class Meta:
        model = "datamodel.Klant"


class ContactMomentFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    zaak = factory.Faker("url")
    kanaal = factory.Faker("word")
    initiatiefnemer = factory.fuzzy.FuzzyChoice(InitiatiefNemer.values)

    class Meta:
        model = "datamodel.ContactMoment"
