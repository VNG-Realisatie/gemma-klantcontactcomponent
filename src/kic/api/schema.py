from django.conf import settings

from drf_yasg import openapi

description = f"""Een API om een klantinteractiecomponent (KIC) te benaderen.

Een KLANTINTERACTIEMOMENT is het abstracte kernobject wat zich concreet
voordoet als CONTACTMOMENT of VERZOEK. Hieraan zijn verschillende andere
resources gerelateerd. De Klantinteracties API kan zelfstandig of met
andere API's samen werken om tot volledige functionaliteit te komen.

**Afhankelijkheden**

Deze API is afhankelijk van:

* Autorisaties API
* Zaken API *(optioneel)*
* Documenten API *(optioneel)*

**Autorisatie**

Deze API vereist autorisatie. Je kan de
[token-tool](https://zaken-auth.vng.cloud/) gebruiken om JWT-tokens te
genereren.

**Handige links**

* [Documentatie]({settings.DOCUMENTATION_URL}/standaard)
* [Zaakgericht werken]({settings.DOCUMENTATION_URL})
"""

info = openapi.Info(
    title=f"{settings.PROJECT_NAME} API",
    default_version=settings.API_VERSION,
    description=description,
    contact=openapi.Contact(
        email="standaarden.ondersteuning@vng.nl", url=settings.DOCUMENTATION_URL,
    ),
    license=openapi.License(
        name="EUPL 1.2", url="https://opensource.org/licenses/EUPL-1.2"
    ),
)
