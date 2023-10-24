#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w17verifica.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W17verificaView)
router.register(r"data", views.W17verificaDataView)
router.register(r"massimali", views.W17verificaMassimaliSerializerView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "html/<int:pk>",
        views.HtmlView.as_view(content_type="text/html"),
        name="w17verifica-html",
    ),
    path("pdf/<int:pk>", views.PdfView.as_view(), name="w17verifica-pdf"),
]
