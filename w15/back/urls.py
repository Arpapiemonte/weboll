#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w15.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W15View)
router.register(r"data", views.W15DataView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.ParchiPDFView.as_view(), name="parchi-pdf"),
    path("html/<int:pk>", views.ParchiHTMLView.as_view(), name="parchi-html"),
    path("png/<int:pk>", views.ParchiPngView.as_view(), name="parchi-png"),
    path(
        "mandria/<int:pk>",
        views.MandriaXmlView.as_view(content_type="text/xml"),
        name="mandria-xml",
    ),
    path(
        "stupinigi/<int:pk>",
        views.StupinigiXmlView.as_view(content_type="text/xml"),
        name="stupinigi-xml",
    ),
]
