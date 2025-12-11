#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w36.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W36View)
router.register(r"data", views.W36DataView)
router.register(r"parametri", views.W36ParametriEquazioneView)
# router.register(r"chart", views.ChartView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "pdf_regione/<int:pk>",
        views.CaldoRegionePDFView.as_view(),
        name="caldo_regione-pdf",
    ),
    path(
        "pdf_torino/<int:pk>",
        views.CaldoTorinoPDFView.as_view(),
        name="caldo_torino-pdf",
    ),
    path(
        "html_regione/<int:pk>",
        views.CaldoRegioneHTMLView.as_view(),
        name="caldo_regione-html",
    ),
    path(
        "html_torino/<int:pk>",
        views.CaldoTorinoHTMLView.as_view(),
        name="caldo_torino-html",
    ),
    path("chart/<int:pk>", views.ChartView.as_view()),
    path(
        "kml_regione/<int:pk>",
        views.KmlView.as_view(content_type="text/plain; charset=windows-1252"),
        name="caldo-regione-kml",
    ),
    path("current/<yyyy-mm-dd:emissione>/", views.W36CurrentView.as_view()),
    # path("png/<int:pk>", views.CaldoPngView.as_view(), name="caldo-png"),
]
