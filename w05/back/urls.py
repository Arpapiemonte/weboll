#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w05.back import views

router = routers.DefaultRouter()
router.register(r"sky_conditions", views.SkyConditionsView)
router.register(r"bulletins", views.W05View)
router.register(r"meteo_classes", views.W05ClassesView)
router.register(r"classes", views.ClassesView)
router.register(r"data", views.W05DataView)
router.register(r"venue_names", views.VenueNamesView)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("pdf/<int:pk>", views.MeteoPDFView.as_view(), name="meteo-pdf"),
    path("svg/<int:pk>", views.MeteoSVGView.as_view(), name="meteo-svg"),
    path(
        "previsione_sst/<int:pk>",
        views.PrevisioneSstView.as_view(
            content_type="text/plain; charset=windows-1252"
        ),
        name="meteo-sst",
    ),
    path(
        "meteo_xml/<int:pk>",
        views.MeteoXmlView.as_view(content_type="text/xml"),
        name="meteo-xml",
    ),
    path("bmp/<int:pk>", views.MeteoBmpView.as_view(), name="meteo-bmp"),
    path("png/<int:pk>", views.MeteoPngView.as_view(), name="meteo-png"),
    path(
        "webarpa/<int:pk>",
        views.MeteoWebarpaView.as_view(content_type="text/xml"),
        name="meteo-webarpa",
    ),
    path(
        "webarpa_old/<int:pk>",
        views.MeteoWebarpaOldView.as_view(content_type="text/xml"),
        name="meteo-webarpa-old",
    ),
]
