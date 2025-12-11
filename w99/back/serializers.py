#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
from rest_framework import serializers

from w35.back import models as models_w35
from w36.back import models as models_w36
from website.core import models as models_w05


class MeteoRealTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models_w36.MeteoRealTime
        fields = "__all__"


class ForecastStationsSerializer(serializers.ModelSerializer):
    count = serializers.ReadOnlyField()
    model_name = serializers.ReadOnlyField(source="id_forecast_run__model_name")
    model_type = serializers.ReadOnlyField(source="id_forecast_run__model_type")
    date_emiss = serializers.ReadOnlyField(source="id_forecast_run__date_emiss")
    time_emiss = serializers.ReadOnlyField(source="id_forecast_run__time_emiss")
    last_update = serializers.ReadOnlyField(source="id_forecast_run__last_update")

    class Meta:
        model = models_w35.ForecastStations
        fields = [
            "count",
            "model_name",
            "model_type",
            "date_emiss",
            "time_emiss",
            "last_update",
        ]


class StazioneMisuraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models_w05.StazioneMisura
        fields = [
            "codice_istat_comune",
            "progr_punto_com",
            "cod_staz_meteo",
            "denominazione",
        ]


class ForecastValuesSerializer(serializers.ModelSerializer):
    station = serializers.SerializerMethodField()
    parameter = serializers.SerializerMethodField()
    date_emiss = serializers.SerializerMethodField()
    time_emiss = serializers.SerializerMethodField()
    # "-id_forecast_parameter__id_forecast_station__id_forecast_run__date_emiss",
    # "-id_forecast_parameter__id_forecast_station__id_forecast_run__time_emiss",

    def get_station(self, obj):
        return obj.id_forecast_parameter.id_forecast_station.cod_staz_meteo

    def get_parameter(self, obj):
        return obj.id_forecast_parameter.id_parametro.id_parametro

    def get_date_emiss(self, obj):
        return obj.id_forecast_parameter.id_forecast_station.id_forecast_run.date_emiss

    def get_time_emiss(self, obj):
        return obj.id_forecast_parameter.id_forecast_station.id_forecast_run.time_emiss

    class Meta:
        model = models_w35.ForecastValues
        fields = [
            "station",
            "parameter",
            "date_emiss",
            "time_emiss",
            "date_rif",
            "time_rif",
            "value",
        ]
