#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w34.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W34View)
router.register(r"data", views.W34DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.CorrierePDFView.as_view(), name="coriere-pdf"),
    path("html/<int:pk>", views.CorriereHTMLView.as_view(), name="coriere-html"),
    path("png/<int:pk>", views.CorrierePngView.as_view(), name="coriere-png"),
]
