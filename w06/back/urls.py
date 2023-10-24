#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w06.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W06View)
router.register(r"data", views.W06DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "svg/<int:pk>",
        views.W06SVGView.as_view(),
        name="w06-svg",
    ),
    path("pdf/<int:pk>", views.W06PDFView.as_view(), name="w06-pdf"),
]
