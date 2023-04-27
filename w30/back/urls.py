#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w30.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W30View)
router.register(r"data", views.W30DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("current/<yyyy-mm-dd:data_emissione>", views.W30CurrentView.as_view()),
    path("currentdata/<yyyy-mm-dd:data_emissione>", views.W30CurrentDataView.as_view()),
    path(
        "html/<int:pk>",
        views.HtmlView.as_view(content_type="text/html"),
        name="psa-html",
    ),
    path("pdf/<int:pk>", views.PdfView.as_view(), name="psa-pdf"),
    path(
        "psa_txt/<int:pk>",
        views.PreviNAView.as_view(
            content_type="text/plain; charset=windows-1252"
            # content_type="text/html; charset=windows-1252"
        ),
        name="psa-txt",
    ),
]
