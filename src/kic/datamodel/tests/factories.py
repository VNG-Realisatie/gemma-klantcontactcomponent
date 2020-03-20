import factory.fuzzy

from ..constants import (
    InitiatiefNemer,
    KlantType,
    ObjectTypes,
    SoortRechtsvorm,
    VerzoekStatus,
)


class KlantFactory(factory.django.DjangoModelFactory):
    voornaam = factory.Faker("first_name")
    achternaam = factory.Faker("last_name")
    adres = factory.Faker("address")
    emailadres = factory.Faker("email")
    functie = factory.Faker("word")
    subject = factory.Faker("url")
    subject_type = factory.fuzzy.FuzzyChoice(KlantType.values)

    class Meta:
        model = "datamodel.Klant"


class ContactMomentFactory(factory.django.DjangoModelFactory):
    bronorganisatie = factory.Faker("ssn", locale="nl_NL")
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
    bronorganisatie = factory.Faker("ssn", locale="nl_NL")
    klant = factory.SubFactory(KlantFactory)
    tekst = factory.Faker("word")
    status = factory.fuzzy.FuzzyChoice(VerzoekStatus.values)

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


class NietNatuurlijkPersoonFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    inn_nnp_id = factory.Faker("ssn", locale="nl_NL")
    statutaire_naam = factory.Faker("word")
    inn_rechtsvorm = factory.fuzzy.FuzzyChoice(SoortRechtsvorm.values)
    bezoekadres = factory.Faker("address", locale="nl_NL")

    class Meta:
        model = "datamodel.NietNatuurlijkPersoon"


class VestigingFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    vestigings_nummer = factory.Sequence(lambda n: f"{n}")
    handelsnaam = factory.List([factory.Faker("word")])

    class Meta:
        model = "datamodel.Vestiging"


class VerzoekProductFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    product = factory.Faker("url")

    class Meta:
        model = "datamodel.VerzoekProduct"


class VerzoekContactMomentFactory(factory.django.DjangoModelFactory):
    verzoek = factory.SubFactory(VerzoekFactory)
    contactmoment = factory.SubFactory(ContactMomentFactory)

    class Meta:
        model = "datamodel.VerzoekContactMoment"


# factories for nested objects
class SubVerblijfBuitenlandFactory(factory.django.DjangoModelFactory):
    natuurlijkpersoon = factory.SubFactory(NatuurlijkPersoonFactory)
    # nietnatuurlijkpersoon = factory.SubFactory(NietNatuurlijkPersoonFactory)
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
