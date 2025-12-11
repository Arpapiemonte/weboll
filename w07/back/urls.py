#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w07.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W07View)
router.register(r"data", views.W07DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "svg_a4/<int:pk>",
        views.W07a4SVGView.as_view(),
        name="w07-a4-svg",
    ),
    path("pdf_a4/<int:pk>", views.W07a4PDFView.as_view(), name="w07-a4-pdf"),
    path(
        "svg_a21/<int:pk>",
        views.W07a21SVGView.as_view(),
        name="w07-a21-svg",
    ),
    path("pdf_a21/<int:pk>", views.W07a21PDFView.as_view(), name="w07-a21-pdf"),
]
