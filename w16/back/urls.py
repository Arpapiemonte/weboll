#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w16.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W16View)
router.register(r"levels", views.OzonoLivelliView)
router.register(r"data", views.W16DataView)
router.register(r"conf", views.W16ConfView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.OzonoPDFView.as_view(), name="ozono-pdf"),
    path("svg/<int:pk>", views.OzonoSVGView.as_view(), name="ozono-svg"),
]
