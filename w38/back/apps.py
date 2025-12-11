#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w38.back"
    label = "w38_back"

    def ready(self):
        import w38.back.signals  # noqa
