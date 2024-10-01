#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
from django.urls import include, path
from rest_framework import routers

from w22.back import views

router = routers.DefaultRouter()
router.register(r"bulletins", views.W22View)
router.register(r"data", views.W22DataView)
router.register(r"zone", views.W22ZoneView)
router.register(r"tendenza", views.W22TendenzaView)
router.register(r"criticita", views.W22CriticitaView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.PienePDFView.as_view(), name="piene-pdf"),
    path("html/<int:pk>", views.PieneHTMLView.as_view(), name="piene-html"),
    path("png/<int:pk>", views.PienePngView.as_view(), name="piene-png"),
    path(
        "kml/<int:pk>",
        views.KmlView.as_view(content_type="text/plain; charset=windows-1252"),
        name="piene-kml",
    ),
]
