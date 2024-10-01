#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w31.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W31View)
router.register(r"data", views.W31DataMacroareeLivelliView)
router.register(r"levels", views.W31LivelliView)


# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("current/<yyyy-mm-dd:emissione>", views.W31CurrentView.as_view()),
    path("pdf/<int:pk>", views.IncendiPDFView.as_view(), name="incendi-pdf"),
    path(
        "svg/<int:pk>",
        views.IncendiSVGView.as_view(),
        name="incendi-svg",
    ),
    path(
        "png/<int:pk>",
        views.IncendiPngView.as_view(),
        name="incendi-png",
    ),
]
