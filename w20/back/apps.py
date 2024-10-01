#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w20.back"
    label = "w20_back"

    def ready(self):
        import w20.back.signals  # noqa
