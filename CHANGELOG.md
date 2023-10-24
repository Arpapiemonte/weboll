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
