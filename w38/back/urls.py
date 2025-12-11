#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w38.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W38View)
router.register(r"data", views.W38DataView)
router.register(r"dataIvrea", views.W38DatiIvreaView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.UviPDFView.as_view(), name="uvi-pdf"),
    path("html/<int:pk>", views.UviHTMLView.as_view(), name="uvi-html"),
    path("png/<int:pk>", views.UviPngView.as_view(), name="uvi-png"),
]
