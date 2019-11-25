import factory.fuzzy

from ..constants import InitiatiefNemer, KlantType, ObjectTypes


class KlantFactory(factory.django.DjangoModelFactory):
    voornaam = factory.Faker("first_name")
    achternaam = factory.Faker("last_name")
    adres = factory.Faker("address")
    emailadres = factory.Faker("email")
    subject = factory.Faker("url")
    subject_type = factory.fuzzy.FuzzyChoice(KlantType.values)

    class Meta:
        model = "datamodel.Klant"


class ContactMomentFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    kanaal = factory.Faker("word")
    initiatiefnemer = factory.fuzzy.FuzzyChoice(InitiatiefNemer.values)
    medewerker = factory.Faker("url")

    class Meta:
        model = "datamodel.ContactMoment"


class ObjectContactMomentFactory(factory.django.DjangoModelFactory):
    contactmoment = factory.SubFactory(ContactMomentFactory)
    object_type = factory.fuzzy.FuzzyChoice(ObjectTypes.values)
    object = factory.Faker("url")

    class Meta:
        model = "datamodel.ObjectContactMoment"


class VerzoekFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    tekst = factory.Faker("word")

    class Meta:
        model = "datamodel.Verzoek"


class ObjectVerzoekFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    object_type = factory.fuzzy.FuzzyChoice(ObjectTypes.values)
    object = factory.Faker("url")

    class Meta:
        model = "datamodel.ObjectVerzoek"


# klant factories
class NatuurlijkPersoonFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    anp_identificatie = factory.Sequence(lambda n: f"{n}")
    geslachtsnaam = factory.Faker("last_name")
    voornamen = factory.Faker("first_name")
    geboortedatum = factory.Faker("date")

    class Meta:
        model = "datamodel.NatuurlijkPersoon"


class VestigingFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    vestigings_nummer = factory.Sequence(lambda n: f"{n}")
    handelsnaam = factory.List([factory.Faker("word")])

    class Meta:
        model = "datamodel.Vestiging"


# factories for nested objects
class SubVerblijfBuitenlandFactory(factory.django.DjangoModelFactory):
    natuurlijkpersoon = factory.SubFactory(NatuurlijkPersoonFactory)
    # vestiging = factory.SubFactory(VestigingFactory)
    lnd_landcode = factory.fuzzy.FuzzyText(length=4)
    lnd_landnaam = factory.Faker("word")

    class Meta:
        model = "datamodel.SubVerblijfBuitenland"


class AdresFactory(factory.django.DjangoModelFactory):
    natuurlijkpersoon = factory.SubFactory(NatuurlijkPersoonFactory)
    # vestiging = factory.SubFactory(VestigingFactory)
    aoa_identificatie = factory.Sequence(lambda n: f"{n}")
    wpl_woonplaats_naam = factory.Faker("city")
    gor_openbare_ruimte_naam = factory.Faker("word")
    aoa_huisnummer = factory.fuzzy.FuzzyInteger(99999)

    class Meta:
        model = "datamodel.Adres"


# ContactMoment Factories
class MedewerkerFactory(factory.django.DjangoModelFactory):
    contactmoment = factory.SubFactory(ContactMomentFactory)
    identificatie = factory.Sequence(lambda n: f"{n}")
    achternaam = factory.Faker("last_name")

    class Meta:
        model = "datamodel.Medewerker"
