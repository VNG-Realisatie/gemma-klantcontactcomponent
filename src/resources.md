# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## ContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/contactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| klant | URL-referentie naar een KLANT (in de KCC API) | string | nee | C​R​U​D |
| datumtijd | De datum en het tijdstip waarop het CONTACTMOMENT begint | string | nee | C​R​U​D |
| kanaal | Het communicatiekanaal waarlangs het CONTACTMOMENT gevoerd wordt | string | nee | C​R​U​D |
| tekst | Een toelichting die inhoudelijk het contact met de klant beschrijft. | string | nee | C​R​U​D |
| initiatiefnemer | De partij die het contact heeft geïnitieerd. | string | nee | C​R​U​D |

## Klant

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klant)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| voornaam |  | string | ja | C​R​U​D |
| achternaam |  | string | ja | C​R​U​D |
| adres |  | string | nee | C​R​U​D |
| telefoonnummer |  | string | nee | C​R​U​D |
| emailadres |  | string | nee | C​R​U​D |
| betrokkene | URL-referentie naar een betrokkene | string | nee | C​R​U​D |
| betrokkeneType | Type van de `betrokkene`.

Uitleg bij mogelijke waarden:

* `natuurlijk_persoon` - Natuurlijk persoon
* `vestiging` - Vestiging | string | ja | C​R​U​D |

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


* Create, Read, Update, Delete
