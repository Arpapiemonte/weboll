#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w15.back"
    label = "w15_back"

    def ready(self):
        import w15.back.signals  # noqa
