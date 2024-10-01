#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w20.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W20View)
router.register(r"data", views.W20DataView)
router.register(r"pericolo", views.W20PericoloView)
router.register(r"zone", views.W20ZoneView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.TrapsPDFView.as_view(), name="traps-pdf"),
    path("html/<int:pk>", views.TrapsHTMLView.as_view(), name="traps-html"),
    path("png/<int:pk>", views.TrapsPngView.as_view(), name="traps-png"),
]
