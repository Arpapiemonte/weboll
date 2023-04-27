#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w29.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W29View)
router.register(r"data", views.W29DataView)
router.register(r"zone", views.W29ZoneView)
router.register(r"pericolo", views.W29PericoloView)
router.register(r"probabilita", views.W29ProbabilitaView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.SlopsPDFView.as_view(), name="slops-pdf"),
    path("html/<int:pk>", views.SlopsHTMLView.as_view(), name="slops-html"),
    path("png/<int:pk>", views.SlopsPngView.as_view(), name="slops-png"),
]
