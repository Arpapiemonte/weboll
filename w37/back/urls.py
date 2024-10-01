#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w37.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W37View)
router.register(r"data", views.W37DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "pdf/<int:pk>", views.AggiornamentoPDFView.as_view(), name="aggiornamento-pdf"
    ),
    path(
        "html/<int:pk>",
        views.AggiornamentoHTMLView.as_view(),
        name="aggiornamento-html",
    ),
    path(
        "png/<int:pk>", views.AggiornamentoPngView.as_view(), name="aggiornamento-png"
    ),
]
