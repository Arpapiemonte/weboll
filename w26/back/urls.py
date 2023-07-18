#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w26.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W26View)
router.register(r"data", views.W26DataView)
router.register(r"bisbulletins", views.BisBollettinoWebolimpiaView)
router.register(r"zone", views.W26ZoneView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "svg/<int:pk>",
        views.W26SVGView.as_view(),
        name="w26-svg",
    ),
    path("pdf/<int:pk>", views.W26PDFView.as_view(), name="w26-pdf"),
]
