#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w37.back"
    label = "w37_back"

    def ready(self):
        import w37.back.signals  # noqa
