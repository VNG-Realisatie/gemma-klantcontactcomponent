# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## Medewerker

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/medewerker)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| identificatie | Een korte unieke aanduiding van de MEDEWERKER. | string | nee | C​R​U​D |
| achternaam | De achternaam zoals de MEDEWERKER die in het dagelijkse verkeer gebruikt. | string | nee | C​R​U​D |
| voorletters | De verzameling letters die gevormd wordt door de eerste letter van alle in volgorde voorkomende voornamen. | string | nee | C​R​U​D |
| voorvoegselAchternaam | Dat deel van de geslachtsnaam dat voorkomt in Tabel 36 (GBA), voorvoegseltabel, en door een spatie van de geslachtsnaam is | string | nee | C​R​U​D |

## ContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/contactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| klant | URL-referentie naar een KLANT (in de Contactmomenten API) indien het contactmoment niet anoniem is. | string | nee | C​R​U​D |
| datumtijd | De datum en het tijdstip waarop het CONTACTMOMENT begint | string | nee | C​R​U​D |
| kanaal | Het communicatiekanaal waarlangs het CONTACTMOMENT gevoerd wordt | string | nee | C​R​U​D |
| tekst | Een toelichting die inhoudelijk het contact met de klant beschrijft. | string | nee | C​R​U​D |
| onderwerpLinks | Eén of meerdere links naar een product, webpagina of andere entiteit zodat contactmomenten gegroepeerd kunnen worden op onderwerp. | array | nee | C​R​U​D |
| initiatiefnemer | De partij die het contact heeft geïnitieerd. | string | nee | C​R​U​D |
| medewerker | URL-referentie naar een medewerker | string | nee | C​R​U​D |

## Klant

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klant)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| voornaam | De voornaam, voorletters of roepnaam van de klant. | string | nee | C​R​U​D |
| achternaam | De achternaam van de klant. | string | nee | C​R​U​D |
| adres | Het adres van de klant. | string | nee | C​R​U​D |
| telefoonnummer | Het mobiele of vaste telefoonnummer van de klant. | string | nee | C​R​U​D |
| emailadres | Het e-mail adres van de klant. | string | nee | C​R​U​D |
| subject | URL-referentie naar een subject | string | nee | C​R​U​D |
| subjectType | Type van de `subject`.

Uitleg bij mogelijke waarden:

* `natuurlijk_persoon` - Natuurlijk persoon
* `vestiging` - Vestiging | string | nee | C​R​U​D |

## SubVerblijfBuitenland

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/subverblijfbuitenland)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| lndLandcode | De code, behorende bij de landnaam, zoals opgenomen in de Land/Gebied-tabel van de BRP. | string | ja | C​R​U​D |
| lndLandnaam | De naam van het land, zoals opgenomen in de Land/Gebied-tabel van de BRP. | string | ja | C​R​U​D |
| subAdresBuitenland1 |  | string | nee | C​R​U​D |
| subAdresBuitenland2 |  | string | nee | C​R​U​D |
| subAdresBuitenland3 |  | string | nee | C​R​U​D |

## NatuurlijkPersoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/natuurlijkpersoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| inpBsn | Het burgerservicenummer, bedoeld in artikel 1.1 van de Wet algemene bepalingen burgerservicenummer. | string | nee | C​R​U​D |
| anpIdentificatie | Het door de gemeente uitgegeven unieke nummer voor een ANDER NATUURLIJK PERSOON | string | nee | C​R​U​D |
| inpANummer | Het administratienummer van de persoon, bedoeld in de Wet BRP | string | nee | C​R​U​D |
| geslachtsnaam | De stam van de geslachtsnaam. | string | nee | C​R​U​D |
| voorvoegselGeslachtsnaam |  | string | nee | C​R​U​D |
| voorletters | De verzameling letters die gevormd wordt door de eerste letter van alle in volgorde voorkomende voornamen. | string | nee | C​R​U​D |
| voornamen | Voornamen bij de naam die de persoon wenst te voeren. | string | nee | C​R​U​D |
| geslachtsaanduiding | Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht nog onbekend is.

Uitleg bij mogelijke waarden:

* `m` - Man
* `v` - Vrouw
* `o` - Onbekend | string | nee | C​R​U​D |
| geboortedatum |  | string | nee | C​R​U​D |

## Vestiging

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/vestiging)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| vestigingsNummer | Een korte unieke aanduiding van de Vestiging. | string | nee | C​R​U​D |
| handelsnaam | De naam van de vestiging waaronder gehandeld wordt. | array | nee | C​R​U​D |

## ObjectContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/objectcontactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| contactmoment | URL-referentie naar het CONTACTMOMENT. | string | ja | C​R​U​D |
| object | URL-referentie naar het gerelateerde OBJECT (in een andere API). | string | ja | C​R​U​D |
| objectType | Het type van het gerelateerde OBJECT.

Uitleg bij mogelijke waarden:

* `zaak` - Zaak | string | ja | C​R​U​D |

## ObjectVerzoek

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/objectverzoek)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| verzoek | URL-referentie naar het VERZOEK. | string | ja | C​R​U​D |
| object | URL-referentie naar het gerelateerde OBJECT (in een andere API). | string | ja | C​R​U​D |
| objectType | Het type van het gerelateerde OBJECT.

Uitleg bij mogelijke waarden:

* `zaak` - Zaak | string | ja | C​R​U​D |

## Verzoek

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/verzoek)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| klant | URL-referentie naar een KLANT (in de Contactmomenten API) indien het contactmoment niet anoniem is. | string | nee | C​R​U​D |
| datumtijd | De datum en het tijdstip waarop het CONTACTMOMENT begint | string | nee | C​R​U​D |
| tekst | Een toelichting die inhoudelijk het contact met de klant beschrijft. | string | nee | C​R​U​D |

## VerzoekInformatieObject

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/verzoekinformatieobject)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| informatieobject | URL-referentie naar het INFORMATIEOBJECT (in de Documenten API) waarin (een deel van) het verzoek beschreven is of aanvullende informatie biedt bij het VERZOEK. | string | ja | C​R​U​D |
| verzoek | URL-referentie naar het VERZOEK. | string | ja | C​R​U​D |


* Create, Read, Update, Delete
