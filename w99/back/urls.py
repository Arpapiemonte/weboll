#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from django.urls import include, path
from rest_framework import routers

from w99.back import views

router = routers.DefaultRouter()
router.register(r"last_models", views.LastModels)
router.register(r"meteo_real_time", views.MeteoRealTime)
router.register(r"forecast_values", views.ForecastValues)
router.register(r"stazione_misura", views.StazioneMisura)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
]
