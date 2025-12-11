#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w23verifica.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W23VerificaView)
router.register(r"data", views.W23VerificaDataView)
router.register(r"zone", views.W23ZoneView)
router.register(r"giudizio", views.W23GiudizioView)
router.register(r"severita", views.W23SeveritaView)
router.register(r"criticita", views.W23verificaCriticitaView)
# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "html/<int:pk>",
        views.VerificaAllertaHTMLView.as_view(content_type="text/html"),
        name="verificaallerta-html",
    ),
    path(
        "pdf/<int:pk>",
        views.VerificaAllertaPDFView.as_view(),
        name="verificaallerta-pdf",
    ),
]
