#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w28.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W28View)
router.register(r"data", views.W28DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "svg/<int:pk>",
        views.W28SVGView.as_view(),
        name="w28-svg",
    ),
    path("pdf/<int:pk>", views.W28PDFView.as_view(), name="w28-pdf"),
]
