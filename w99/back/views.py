#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime

# import tempfile
# from contextlib import closing
# from subprocess import call
from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from w35.back import models as models_w35
from w36.back import models as models_w36
from w99.back.serializers import (
    ForecastStationsSerializer,
    ForecastValuesSerializer,
    MeteoRealTimeSerializer,
    StazioneMisuraSerializer,
)
from website.core import models as models_w05


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class LastModels(viewsets.ModelViewSet):
    queryset = models_w35.ForecastStations.objects.all()

    # https://stackoverflow.com/questions/19707237/use-get-queryset-method-or-set-queryset-variable
    # https://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):
        today = datetime.datetime.today()
        queryset = (
            models_w35.ForecastStations.objects.all()
            .filter(id_forecast_run__date_emiss=today)
            .select_related("id_forecast_run")
            .values(
                "id_forecast_run__model_name",
                "id_forecast_run__model_type",
                "id_forecast_run__date_emiss",
                "id_forecast_run__time_emiss",
                "id_forecast_run__last_update",
            )
            .annotate(count=Count("cod_staz_meteo"))
            .filter(count__gte=100)
            .order_by("-id_forecast_run__date_emiss", "-id_forecast_run__time_emiss")
        )
        return queryset

    # queryset._result_cache = None
    # print(queryset.count())
    serializer_class = ForecastStationsSerializer
    permission_classes = [ReadOnly]


class MRTFilter(filters.FilterSet):
    codice_istat_comune = filters.CharFilter(
        field_name="codice_istat_comune", lookup_expr="exact"
    )
    progr_punto_com = filters.NumberFilter(
        field_name="progr_punto_com", lookup_expr="exact"
    )
    id_parametro = filters.CharFilter(field_name="id_parametro", lookup_expr="exact")

    class Meta:
        model = models_w36.MeteoRealTime
        fields = ["codice_istat_comune", "progr_punto_com", "id_parametro"]


class MeteoRealTime(viewsets.ModelViewSet):
    twodaysago = datetime.datetime.today() - datetime.timedelta(days=2)
    queryset = models_w36.MeteoRealTime.objects.filter(data__gte=twodaysago).order_by(
        "data", "ora"
    )
    serializer_class = MeteoRealTimeSerializer
    permission_classes = [ReadOnly]
    filterset_class = MRTFilter


class StazioneMisura(viewsets.ModelViewSet):
    queryset = models_w05.SensoreStazioneMisura.objects.filter(
        id_parametro="TERMA"
    ).order_by("denominazione")
    serializer_class = StazioneMisuraSerializer
    permission_classes = [ReadOnly]


class ForecastValues(viewsets.ModelViewSet):
    queryset = models_w35.ForecastValues.objects.all()

    # https://stackoverflow.com/questions/19707237/use-get-queryset-method-or-set-queryset-variable
    # https://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):
        forecast_values = []  # type: ignore
        model_name = self.request.GET.get("model_name", "MULTMODEL")
        cod_staz_meteo = self.request.GET.get("cod_staz_meteo", "94061")
        id_parametro = self.request.GET.get("id_parametro", "TERMA")
        time_emiss = self.request.GET.get("time_emiss", "07:35:00")
        print("get_queryset", model_name, cod_staz_meteo, id_parametro)
        today = datetime.datetime.today()
        if (
            models_w35.ForecastStations.objects.select_related("id_forecast_run")
            .values(
                "id_forecast_run__date_emiss",
                "id_forecast_run__time_emiss",
                "id_forecast_run__id_forecast_run",
                "id_forecast_run__model_name",
            )
            .filter(cod_staz_meteo=cod_staz_meteo)
            .filter(id_forecast_run__model_name=model_name)
            .filter(id_forecast_run__date_emiss=today)
            .filter(id_forecast_run__time_emiss=time_emiss)
            .annotate(
                Count("id_forecast_run__date_emiss"),
                Count("id_forecast_run__time_emiss"),
                Count("id_forecast_run__id_forecast_run"),
                Count("id_forecast_run__model_name"),
            )
            .exists()
        ):
            forecast_stations = (
                models_w35.ForecastStations.objects.select_related("id_forecast_run")
                .values(
                    "id_forecast_run__date_emiss",
                    "id_forecast_run__time_emiss",
                    "id_forecast_run__id_forecast_run",
                    "id_forecast_run__model_name",
                )
                .filter(cod_staz_meteo=cod_staz_meteo)
                .filter(id_forecast_run__model_name=model_name)
                .filter(id_forecast_run__date_emiss=today)
                .filter(id_forecast_run__time_emiss=time_emiss)
                .annotate(
                    Count("id_forecast_run__date_emiss"),
                    Count("id_forecast_run__time_emiss"),
                    Count("id_forecast_run__id_forecast_run"),
                    Count("id_forecast_run__model_name"),
                )
                .order_by(
                    "-id_forecast_run__date_emiss", "-id_forecast_run__time_emiss"
                )
                .latest("id_forecast_run__id_forecast_run")
            )
            print("get_queryset forecast_stations", forecast_stations)
            daft = today + datetime.timedelta(days=2)
            forecast_values = (
                models_w35.ForecastValues.objects.select_related("id_forecast_parameter")  # type: ignore
                .select_related("id_forecast_parameter__id_forecast_station")
                .select_related(
                    "id_forecast_parameter__id_forecast_station__id_forecast_run"
                )
                .filter(id_forecast_parameter__id_parametro=id_parametro)
                .filter(id_forecast_parameter__id_aggregazione=0)
                .filter(date_rif__gte=today, date_rif__lte=daft)
                .filter(
                    id_forecast_parameter__id_forecast_station__id_forecast_run=forecast_stations[
                        "id_forecast_run__id_forecast_run"
                    ]
                )
                .filter(
                    id_forecast_parameter__id_forecast_station__cod_staz_meteo=cod_staz_meteo
                )
                .order_by(
                    "-id_forecast_parameter__id_forecast_station__id_forecast_run__date_emiss",
                    "-id_forecast_parameter__id_forecast_station__id_forecast_run__time_emiss",
                )
            )
        print("get_queryset forecast_values", forecast_values)
        return forecast_values

    serializer_class = ForecastValuesSerializer
    permission_classes = [ReadOnly]
