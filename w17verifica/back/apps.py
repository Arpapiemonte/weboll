#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w17verifica.back"
    label = "w17verifica_back"

    def ready(self):
        import w17verifica.back.signals  # noqa
