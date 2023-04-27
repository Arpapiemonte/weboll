#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

import datetime

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.generic import View
from rest_framework import pagination, status
from rest_framework.exceptions import APIException

from config import version


class VersionView(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        response = JsonResponse(
            {
                "stamp": datetime.datetime.utcnow().isoformat(),
                "version": version.__version__,
                "release_date": version.__date__,
            }
        )
        return response


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 31


class ExistingTodayBulletin(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "There is already a bulletin for today."
    default_code = "permission_denied"


class BulletinDraftLocked(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Another user is working on the bulletin draft."
    default_code = "permission_denied"
