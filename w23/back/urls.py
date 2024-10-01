#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w23.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W23View)
router.register(r"data", views.W23DataView)
router.register(r"zone", views.W23ZoneView)
router.register(r"pericoli", views.W23PericoloView)
router.register(r"effetti", views.W23EffettiterritorioView)
router.register(r"time_layouts", views.TimeLayoutsView)
router.register(r"soglie_nivo_area_prev", views.SoglieNivoAreaPrevView)
router.register(r"soglie_pluv_area_prev_massimi", views.SogliePluvAreaPrevMassimiView)
router.register(r"soglie_pluv_area_prev_medie", views.SogliePluvAreaPrevMedieView)
router.register(r"pluvossh6", views.W23Pluvossh6View)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("current/<yyyy-mm-dd:data_emissione>", views.W23CurrentView.as_view()),
    path("pdf/<int:pk>", views.AllertaPDFView.as_view(), name="allerta-pdf"),
    path("html/<int:pk>", views.AllertaHtmlView.as_view(), name="allerta-html"),
    path(
        "rupar_pdf/<int:pk>",
        views.AllertaPDFView.as_view(template_name="allerta_rupar.html"),
        name="allerta-rupar-html",
    ),
    path(
        "rupar_html/<int:pk>",
        views.AllertaHtmlView.as_view(template_name="allerta_rupar.html"),
        name="allerta-rupar-html",
    ),
    path(
        "rupar_png/<int:pk>",
        views.AllertaPngView.as_view(template_name="allerta_rupar.html"),
        name="allerta-rupar-png",
    ),
    path(
        "png/<int:pk>",
        views.AllertaPngOrigView.as_view(template_name="allerta_rupar.html"),
        name="allerta-png",
    ),
    path(
        "kml/<int:pk>",
        views.KmlView.as_view(content_type="text/plain; charset=windows-1252"),
        name="allerta-kml",
    ),
    path(
        "kml36h/<int:pk>",
        views.Kml36hView.as_view(content_type="text/plain; charset=windows-1252"),
        name="allerta-kml",
    ),
    path(
        "xml/<int:pk>",
        views.XmlView.as_view(content_type="text/plain; charset=utf-8"),
        name="allerta-xml",
    ),
]
