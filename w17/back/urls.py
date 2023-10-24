#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w17.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W17View)
router.register(r"classes", views.W17ClassesView)
router.register(r"data", views.W17DataView)
router.register(r"stazioni", views.StazioneMisura)
router.register(r"trend", views.Trend)
router.register(r"bulletins_full", views.W17FullView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "svg/<int:pk>",
        views.W17SVGView.as_view(),
        name="w17-svg",
    ),
    path("pdf/<int:pk>", views.W17PDFView.as_view(), name="w17-pdf"),
]
