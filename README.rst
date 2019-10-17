========================
Klantcontactcomponent
========================

:Version: 0.1.0
:Source: https://github.com/VNG-Realisatie/gemma-klantcontactcomponent
:Keywords: zaken, zaakgericht werken, GEMMA, KCC
:PythonVersion: 3.6

|build-status|

Referentieimplementatie van de klantcontactcomponent (KCC).

Inleiding
=========

Binnen het Nederlandse gemeentelandschap wordt zaakgericht werken nagestreefd.
Om dit mogelijk te maken is er gegevensuitwisseling nodig. De kerngegevens van
zaken moeten ergens geregistreerd worden en opvraagbaar zijn.

Deze referentieimplementatie toont aan dat de API specificatie voor de
klantcontactcomponent (hierna KCC) implementeerbaar is, en vormt een
voorbeeld voor andere implementaties indien ergens twijfel bestaat.

Deze component heeft ook een `testomgeving`_ waar leveranciers tegenaan kunnen
testen.

Documentatie
============

Zie ``INSTALL.rst`` voor installatieinstructies, beschikbare instellingen en
commando's.

Indien je actief gaat ontwikkelen aan deze component raden we aan om niet van
Docker gebruik te maken. Indien je deze component als black-box wil gebruiken,
raden we aan om net wel van Docker gebruik te maken.

Referenties
===========

* `Issues <https://github.com/VNG-Realisatie/gemma-klantcontactcomponent/issues>`_
* `Code <https://github.com/VNG-Realisatie/gemma-klantcontactcomponent>`_


.. |build-status| image:: http://jenkins.nlx.io/buildStatus/icon?job=gemma-klantcontactcomponent-stable
    :alt: Build status
    :target: http://jenkins.nlx.io/job/gemma-klantcontactcomponent-stable

.. |requirements| image:: https://requires.io/github/VNG-Realisatie/gemma-klantcontactcomponent/requirements.svg?branch=master
     :target: https://requires.io/github/VNG-Realisatie/gemma-klantcontactcomponent/requirements/?branch=master
     :alt: Requirements status

.. _testomgeving: https://ref.tst.vng.cloud/ABBREVIATION/

Licentie
========

Copyright © VNG Realisatie 2019

Licensed under the EUPL_

.. _EUPL: LICENCE.md
