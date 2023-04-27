#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = "w05.back"
    label = "w05_back"

    def ready(self):
        import w05.back.signals  # noqa
