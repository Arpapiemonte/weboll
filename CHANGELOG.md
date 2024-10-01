# 1.5.0 (2024-09-30)

## Features

- General:
  - send bulletin via email
  - send email in case of error on file shipments
  - debian 12: default font changed use Liberation Sans
  - switch to the ergonomic defineEmits in TypeScript
  - pass bulletin id as a prop in TypeScript
  - ssh with options
  - send email with django
  - added the highways sections altitude on the frontend
  - collapse buttons in home page for menu item
  - celery tasks results integrated in django
  - new celery task send auto destination
  - remove vee-validate
  - show date of the last sent or reopened bulletin in home page
  - reopen bulletin everywhere
  - new model compare utility

- Autostrade:
  - a7-a26 export the forecast xml file

- new Traps bulletin

- new Corriere di Novara bulletin

- new Strade di Biella bulletin

- new forecasts on weather areas bulletin

- new forecasts Parchi Reali

- new Aggiornamento Allerta bulletin

- new Ondate di calore bulletin

- Allerta
  - export kml
  - export xml
  - automatic full sentence for plumbing alert

- Piene:
  - reopen bulletin
  - export kml

- Analisi bulletin:
  - pdf review
  - station altitude in front

- Bollettino meteo:
  - check snow level
  - export kml

- Vigilanza
  - add png export button

## Bugfixes

- General:
  - Fix homepage
  - send when saving finishes
  - restore correct bootstrap imports
  - get Titillium Font locally
  - Fix crontab task auto and send if bulletin time between -5 and + 5 minutes
  - stazionemisura model defined only once

- Autostrade:
  - a7-a26 risk_freezing_rain into PDF, accept 0/8 of cloud cover
  - a6 set risk_freezing_rain to False
  - all highways wrong date on the third day

- Verifica meteo:
  - error in saving
  - visibility incorrect points
  - check the cells that do not get the max points must be bordered in red
  - fix various errors

- Verifica piene
  - does not effectively save the criterion and excellent judgment is missing
  - fix judgment

- Vigilanza:
  - bug on the prev column average in 6h and snow share in the snowfall box
  - Fix mypy error
  - Catch exception when PSA does not exists
  - don't save Nan
  - Fix snow level
  - Fix png end-point

- PSA:
  - delete the forecast_zone from the psa send

- Analisi bulletin:
  - W17 front typescript error
  - fix pdf template
  - fix morning instead of afternoon

- BIS
  - Fix box coloring query
  - Fix bulletin number based on validity date

- Incendi
  - Sort the areas as in the pdf and correct spelling errors in the pdf legend
  - if there are no data build empty bulletin

- Meteo
  - Fix save correct snow_level aggregations

- Allerta
  - Fix snow level labels
  - Fix if data in pluvoss is missing
  - Fix warning columns not consistent between the various products
  - The scenario column can be written and must not be deleted
  - The note must not erase what has been written

- Piene
  - Fix the time windows

# 1.4.0 (2023-10-18)

## Features

- General:

  - New Autostrada A4-A21 bulletin

  - New Autostrada A33 bulletin

  - New Autostrada A6 bulletin

  - New Drop down menù

  - the backend creates a fake response to give feedback

- Incendi bulletin:
  - Fires zone name change, more logs in console

- BIS bulletin:
  - send_with_celery for BIS date of file must be the validity date
  - station replacement Busca with Dronero
  - change description of BIS notes

- Analisi bulletin:
  - w17 tables dumps
  - freezing level values ​​in the analysis: increase/decrease with arrows at 100 m intervals and not units

- Autostrade bulletin:
  - new very heavy snow icon
  - handle null value

- Verifica Meteo bulletin:
  - graphic adjustments

## Bugfixes

- General:
  - debian 12: default font changed workaround
  
- Autostrade bulletins:
  - w12, w17 ,w26 e w33 add signals
  - w26.pdf instead of w12.pdf
  - a7-a26 reopened bulletins must not be considered by the new
  - a7-a26 error in precipitation intensity association
  - a7-a26 pdf: replace TRUE with YES
  - pdf correct header field
  - insert check that with snow icons you do not accept snow level to null
  - PDF Highways. Headers, logos and miscellaneous

- BIS bulletin:
  - correction of BIS bulletin number
  - on the PDF, the issue date and validity date are the same
  - remove bold

- Metaprodotto bulletin:
  - if I select WIND AND SNOW, when I enter the cumulative snow value the snow and snow depth boxes disappear

- Analisi bulletin:
  - as soon as the bulletin is opened the first tab is empty and fetchAnalisiData gives an error
  - drop-down menus not pre-populated
  - min/max temperature trend not calculated
  - the fields of the min/max snow level are missing
  - a null temperature value is not handled (puts zero and not null/n.d.)
  - the ANALYSIS DATE is missing from the bulletin list

- PSA bulletin:
  - HTML export broken
  - the export in previNA_20231009.txt must be sorted by area

- Verifica Meteo bulletin:
  - intensity and wind trend values ​​exchanged
  - it doesn't handle properly if analysis is missing
  - observed max and min temperature trend not present
  - graphic adjustments

- Piene
  - wrong Lago all-time level

# 1.3.0 (2023-07-17)

## Features

- New BIS (_Bollettino Idrologico di Sintesi_) bulletin

- New Metaprodotto bulletin

- New Autostrada A26-A7 bulletin

- New Analisi Meteo bulletin

- New Verifica Meteo bulletin

- Allerta bulletin:

  - buttons to manually get all output formats

- Fire bulletin:

  - add foehn icon

## Bugfixes

- General:

  - upgrade the container base images to Debian 12 and node 18; requires [a fix for ImageMagick](https://bugs.debian.org/964090) and switching [from PerceptualDiff to ImageMagick for integration test screenshotting](https://needle.readthedocs.io/en/latest/#engines)
  - refresh JS/TS dependencies, including TypeScript 5
  - upgrade to Django 4.1 + refresh the other Python deps
  - Django ASGI integration
  - fix mypy errors and remove unused code
  - improve publiccode.yml
  - for the CI use images from our registry to avoid error building hitting docker registry's pull rate limit
  - release script also updates publiccode.yml

- Meteo bulletin:

  - sort meteo class descriptors

- Allerta bulletin:

  - _visualizza_ -> _visualizza / modifica_
  - _frase Risknat_ -> _frase sito Arpa_
  - increase size of listbox Scenario atteso
  - fix micro-maps coloring
  - also save max precipitation to DB

- Bollettino Piene:

  - fix max date
  - fix thresholds can be null
  - new massimo_previsione

- Slops bulletin:

  - _zone_ -> _aree_
  - minor spacing added in caption

- Vigilanza bulletin:

  - fix layout hot thermal anomaly 1<sup>st</sup> day

- Fire bulletin:

  - change sending time to 12:00

- PSA bulletin:

  - fix "_Copia scadenza_" for _Zero termico_ and _Quota neve_
  - ask user to confirm "_Copia valori modello_"

# 1.2.0 (2023-05-18)

First public release.
