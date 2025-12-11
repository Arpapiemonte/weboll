#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w22verifica.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W22VerificaView)
router.register(r"data", views.W22VerificaDataView)
router.register(r"zone", views.W22ZoneView)
router.register(r"giudizio", views.W22GiudizioView)
router.register(r"severita", views.W22SeveritaView)
router.register(r"criticita", views.W22verificaCriticitaView)
# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "html/<int:pk>",
        views.VerificaPieneHTMLView.as_view(content_type="text/html"),
        name="verificapiene-html",
    ),
    path(
        "pdf/<int:pk>", views.VerificaPienePDFView.as_view(), name="verificapiene-pdf"
    ),
]
