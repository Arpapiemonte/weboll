# 1.3.0 (2023-07-17)

## Features

- New BIS (_Bollettino Idrologico di Sintesi_) bulletin

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
