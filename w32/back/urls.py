#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w32.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W32View)
router.register(r"data", views.W32DataView)
router.register(r"datambacini", views.W32MbaciniDataView)
router.register(r"zone", views.W32ZoneView)
router.register(r"pericolo", views.W32PericoloView)
router.register(r"pericolombacini", views.W32PericolombaciniView)
router.register(r"mbacini", views.W32MbaciniView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.DefensePDFView.as_view(), name="defense-pdf"),
    path("html/<int:pk>", views.DefenseHTMLView.as_view(), name="defense-html"),
    path("png/<int:pk>", views.DefensePngView.as_view(), name="defense-png"),
    path("pdf_frane/<int:pk>", views.FranePDFView.as_view(), name="frane-pdf"),
    path("html_frane/<int:pk>", views.FraneHTMLView.as_view(), name="frane-html"),
]
