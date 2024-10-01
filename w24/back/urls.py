#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w24.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W24View)
router.register(r"data", views.W24DataView)
router.register(r"soglie", views.W24SoglieView)
router.register(r"fz", views.ForecastZoneView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("current/<yyyy-mm-dd:data_emissione>", views.W24CurrentView.as_view()),
    path("pdf/<int:pk>", views.VigilanzaPDFView.as_view(), name="vigilanza-pdf"),
    path("html/<int:pk>", views.VigilanzaHTMLView.as_view(), name="vigilanza-html"),
    path(
        "rupar_pdf/<int:pk>",
        views.VigilanzaPDFView.as_view(template_name="vigilanza_rupar.html"),
        name="vigilanza-rupar-html",
    ),
    path(
        "rupar_html/<int:pk>",
        views.VigilanzaHTMLView.as_view(template_name="vigilanza_rupar.html"),
        name="vigilanza-rupar-html",
    ),
    path(
        "rupar_png/<int:pk>",
        views.VigilanzaPngRuparView.as_view(template_name="vigilanza_rupar.html"),
        name="vigilanza-rupar-png",
    ),
    path(
        "png/<int:pk>",
        views.VigilanzaPngView.as_view(template_name="vigilanza.html"),
        name="vigilanza-png",
    ),
]
