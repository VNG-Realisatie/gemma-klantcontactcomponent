# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## ContactMoment

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/contactmoment)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| klant |  | string | nee | C​R​U​D |
| zaak | URL-referentie naar de ZAAK (in de Zaken API) | string | nee | C​R​U​D |
| datumtijd | De datum en het tijdstip waarop het CONTACTMOMENT begint | string | nee | C​R​U​D |
| kanaal | Het communicatiekanaal waarlangs het CONTACTMOMENT gevoerd wordt | string | nee | C​R​U​D |
| text | Een toelichting die inhoudelijk het contact met de klant beschrijft. | string | nee | C​R​U​D |

## Klant

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klant)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| voornaam |  | string | ja | C​R​U​D |
| achternaam |  | string | ja | C​R​U​D |
| adres |  | string | nee | C​R​U​D |
| telefonnummer |  | string | nee | C​R​U​D |
| emailadres |  | string | nee | C​R​U​D |


* Create, Read, Update, Delete
