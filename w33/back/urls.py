#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w33.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W33View)
router.register(r"data", views.W33DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "html/<int:pk>",
        views.HtmlView.as_view(content_type="text/html"),
        name="psa-html",
    ),
    path("pdf/<int:pk>", views.PdfView.as_view(), name="mpa-pdf"),
]
