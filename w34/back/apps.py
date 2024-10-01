#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w34.back"
    label = "w34_back"

    def ready(self):
        import w34.back.signals  # noqa
