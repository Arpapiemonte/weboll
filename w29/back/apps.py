#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w29.back"
    label = "w29_back"

    def ready(self):
        import w29.back.signals  # noqa
