#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w21.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W21View)
router.register(r"data", views.W21DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "svg/<int:pk>",
        views.W21SVGView.as_view(),
        name="w21-svg",
    ),
    path("pdf/<int:pk>", views.W21PDFView.as_view(), name="w21-pdf"),
    path("png/<int:pk>", views.W21PngView.as_view(), name="w21-png"),
]
