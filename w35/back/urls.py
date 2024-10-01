#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w35.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W35View)
router.register(r"data", views.W35DataView)
router.register(r"aree_meteo", views.AreeMeteoView)
router.register(r"tasks", views.TasksView)
router.register(r"forecast_comuni", views.ForecastComuniView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "html/<int:pk>",
        views.HtmlView.as_view(content_type="text/html"),
        name="w35-html",
    ),
    path("pdf/<int:pk>", views.PdfView.as_view(), name="w35-pdf"),
]