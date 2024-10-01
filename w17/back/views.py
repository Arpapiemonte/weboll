#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

import datetime
import json
import os
from base64 import b64encode

import requests
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from w17.back import models
from w17.back.serializers import (
    StazioneMisuraSerializer,
    TrendSerializer,
    W17ClassesSerializer,
    W17DataSerializer,
    W17Serializer,
    W17SerializerFull,
)
from website.common.tasks import send_with_celery
from website.common.views import BulletinDraftLocked, StandardResultsSetPagination
from website.core import models as models_w05


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W17ClassesView(viewsets.ModelViewSet):
    """
    API endpoint that allows W17 classes to be viewed
    """

    queryset = models.W17Classes.objects.all()
    serializer_class = W17ClassesSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W17DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W17 bulletin Data to be viewed or edited
    """

    queryset = models.W17Data.objects.all()
    serializer_class = W17DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W17Data.objects
        w17Data = get_object_or_404(queryset, pk=pk)
        serializer = W17DataSerializer(w17Data, context={"request": request})
        return Response(serializer.data)


class W17Filter(filters.FilterSet):
    # data_min = filters.DateTimeFilter(field_name="start_valid_time", lookup_expr="gte")
    # data_max = filters.DateTimeFilter(field_name="start_valid_time", lookup_expr="lte")
    data = filters.DateTimeFilter(field_name="data_analysis")

    class Meta:
        model = models.W17
        fields = ["data"]


class W17FullView(viewsets.ModelViewSet):
    queryset = models.W17.objects.order_by("-last_update", "numero_bollettino", "-pk")
    serializer_class = W17SerializerFull
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_class = W17Filter


class StazioneMisura(viewsets.ModelViewSet):
    """
    API endpoint that allows stations to be viewed
    """

    queryset = models_w05.StazioneMisura.objects.all()
    serializer_class = StazioneMisuraSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class Trend(viewsets.ModelViewSet):
    """
    API endpoint that allows trends to be viewed
    """

    queryset = models_w05.Trend.objects.all()
    serializer_class = TrendSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W17View(viewsets.ModelViewSet):
    """
    API endpoint that allows W17 bulletins to be viewed or edited
    """

    queryset = models.W17.objects.order_by("-last_update", "-pk")
    serializer_class = W17Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        month = self.request.query_params.get("month", "all")
        year = self.request.query_params.get("year", "all")
        if month != "all":
            queryset = (
                self.get_queryset()
                .filter(data_emissione__year=year)
                .filter(data_emissione__month=month)
            )
        elif year != "all":
            queryset = self.filter_queryset(
                self.get_queryset().filter(data_emissione__year=year)
            )
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W17.objects
        if (
            instance.id_w17_parent
            and queryset.filter(pk=instance.id_w17_parent).exists()
        ):
            w17 = get_object_or_404(queryset, pk=instance.id_w17_parent)
            w17.status = "1"
            if not User.objects.filter(username=w17.username).exists():
                print("perform_destroy non trovo l'utente " + w17.username)
                w17.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w17.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W17.objects
        w17 = get_object_or_404(queryset, pk=pk)
        serializer = W17SerializerFull(w17, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # crea il nuovo bollettino di oggi
        delimiter = "__"

        def HashW17Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
            return (
                str(id_venue)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(id_time_layouts)
            )

        def HashW17Classes(id_parametro, id_time_layouts, id_classes):
            return (
                id_parametro
                + delimiter
                + str(id_time_layouts)
                + delimiter
                + str(id_classes)
            )

        def PrecClassMedia(prec_value):
            result = None
            if prec_value < 0.5:
                result = 16
            elif prec_value >= 0.5 and prec_value < 10:
                result = 17
            elif prec_value >= 10 and prec_value < 30:
                result = 18
            elif prec_value >= 30 and prec_value < 60:
                result = 19
            elif prec_value >= 60:
                result = 20
            return str(result)

        def PrecClassMaxArea(prec_value):
            result = None
            if prec_value < 0.5:
                result = 21
            elif prec_value >= 0.5 and prec_value < 10:
                result = 22
            elif prec_value >= 10 and prec_value < 30:
                result = 23
            elif prec_value >= 30 and prec_value < 60:
                result = 24
            elif prec_value >= 60:
                result = 25
            return str(result)

        def PrecClassMax(prec_value):
            result = None
            if prec_value < 0.5:
                result = 26
            elif prec_value >= 0.5 and prec_value < 10:
                result = 27
            elif prec_value >= 10 and prec_value < 30:
                result = 28
            elif prec_value >= 30 and prec_value < 60:
                result = 29
            elif prec_value >= 60:
                result = 30
            return str(result)

        def WindClassPianura(wind_value):
            result = None
            if wind_value < 1:
                result = 57
            elif wind_value >= 1 and wind_value < 5:
                result = 58
            elif wind_value >= 5 and wind_value < 10:
                result = 59
            elif wind_value >= 10 and wind_value < 15:
                result = 60
            elif wind_value >= 15:
                result = 61
            return str(result)

        def WindClassMontagna(wind_value):
            result = None
            if wind_value < 1:
                result = 66
            elif wind_value >= 1 and wind_value < 5:
                result = 67
            elif wind_value >= 5 and wind_value < 10:
                result = 68
            elif wind_value >= 10 and wind_value < 15:
                result = 69
            elif wind_value >= 15:
                result = 70
            return str(result)

        # set url
        url = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")

        now = datetime.datetime.now()
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)

        # prendi il file per i valori di visibilità
        visibilita_ok = False
        visibilita_analisi_meteo_request = requests.get(
            url + "/analisi/visibilita_analisi_meteo.json"
        )
        if visibilita_analisi_meteo_request.status_code == 200:
            visibilita_analisi_meteo = visibilita_analisi_meteo_request.json()
            if len(visibilita_analisi_meteo) == 3:
                if "data_analisi" in visibilita_analisi_meteo:
                    if visibilita_analisi_meteo["data_analisi"] == yesterday.strftime(
                        "%Y-%m-%d"
                    ):
                        visibilita_ok = True
                    else:
                        print("analisi NON di ieri")
                else:
                    print(
                        "non trovo data_analisi nel file visibilita_analisi_meteo.json"
                    )
            else:
                print(
                    "il file visibilita_analisi_meteo.json non ha la struttura corretta"
                )
        else:
            print("non trovo il file visibilita_analisi_meteo.json")

        emissione = today.replace(hour=12, minute=30, second=0, microsecond=0)
        next_blt_time = emissione + datetime.timedelta(days=1)
        old = (
            models.W17.objects.filter(status="1").order_by("-last_update").latest("pk")
        )
        # gestione anno nuovo
        if old.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            last_seq_num_year = today.year
            new_seq = "1" + "/" + str(last_seq_num_year)
        else:
            last_seq_num = (
                models.W17.objects.filter(data_emissione__year=today.year)
                .exclude(status="0")
                .order_by("-last_update")[0]
                .numero_bollettino
            )
            last_seq_num_year = int(last_seq_num.split("/")[1])
            last_seq_num = last_seq_num.split("/")[0]
            new_seq = str(int(last_seq_num) + 1)
            new_seq = str(new_seq) + "/" + str(last_seq_num_year)

        new = models.W17(
            numero_bollettino=new_seq,
            data_emissione=emissione,
            next_blt_time=next_blt_time,
            data_analysis=yesterday,
            status=0,
            last_update=now,
            username=request.user,
            situation="",
            cloudiness="",
            weather_code="",
        )
        new.save()

        # leggo venues
        fine = datetime.datetime.now()
        print(
            "leggo venues ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        venues = models.Venue.objects.all()
        venues_dict = {}
        for v in venues:
            venues_dict[str(v.id_venue)] = v

        # leggo time layouts
        fine = datetime.datetime.now()
        print(
            "leggo time_layouts ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for t in time_layouts:
            time_layouts_dict[str(t.id_time_layouts)] = t

        # leggo parametro
        fine = datetime.datetime.now()
        print(
            "leggo parametro ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        parametri = models.Parametro.objects.all().select_related("id_unita_misura")
        parametri_dict = {}
        for p in parametri:
            parametri_dict[p.id_parametro] = p

        # leggo aggregazione
        fine = datetime.datetime.now()
        print(
            "leggo aggregazione ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        aggregazione = models.Aggregazione.objects.all().select_related(
            "id_unita_misura"
        )
        aggregazione_dict = {}
        for a in aggregazione:
            aggregazione_dict[str(a.id_aggregazione)] = a

        # leggo weather_values
        fine = datetime.datetime.now()
        print(
            "leggo weather_values ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        weather_values = models_w05.WeatherValues.objects.all().select_related(
            "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
        )
        weather_values_dict = {}
        for w in weather_values:
            weather_values_dict[
                HashW17Data(
                    w.id_venue.id_venue,
                    w.id_parametro.id_parametro,
                    w.id_aggregazione.id_aggregazione,
                    w.id_time_layouts.id_time_layouts,
                )
            ] = w

        # leggo classes
        fine = datetime.datetime.now()
        print(
            "leggo classes ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        classes = models.Classes.objects.all().select_related("id_parametro")
        classes_dict = {}
        for c in classes:
            classes_dict[str(c.id_classes)] = c

        # leggo classes_value
        fine = datetime.datetime.now()
        print(
            "leggo classes_value ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        classes_value = models.ClassesValue.objects.all().select_related("id_classes")
        classes_value_dict: dict = {}
        for cc in classes_value:
            classes_value_dict[str(cc.id_classes_value)] = cc

        # carico la configurazione json per sapere quanti record ci devono essere su w17_data
        with open("config/w17_data.json") as json_file:
            w17_data_config = json.load(json_file)
        # sistema il json di configurazione in modo da avere come chiave primaria
        # id_venue__id_parametro__id_aggregazione__id_time_layouts
        w17_data_da_inserire = {}  # type: ignore
        for w in w17_data_config:
            w17_data_da_inserire[
                HashW17Data(
                    w17_data_config[w]["id_venue"],
                    w17_data_config[w]["id_parametro"],
                    w17_data_config[w]["id_aggregazione"],
                    w17_data_config[w]["id_time_layouts"],
                )
            ] = None

        # creo tutti i w17_data nuovi
        w17_data_new_dict: dict = {}
        for w in w17_data_da_inserire:
            w17_data_tmp = w.split(delimiter)  # type: ignore
            my_time_layouts = time_layouts_dict[w17_data_tmp[3]]
            text_value = None
            w17_data_new_dict[
                HashW17Data(
                    w17_data_tmp[0], w17_data_tmp[1], w17_data_tmp[2], w17_data_tmp[3]
                )
            ] = models.W17Data(
                id_w17=new,
                id_venue=venues_dict[w17_data_tmp[0]],
                id_parametro=parametri_dict[w17_data_tmp[1]],
                id_aggregazione=aggregazione_dict[w17_data_tmp[2]],
                numeric_value=None,
                id_trend=None,
                text_value=text_value,
                id_time_layouts=my_time_layouts,
                cod_staz_meteo=None,
            )

        # carico la configurazione json per sapere quanti record ci devono essere su w17_classes
        with open("config/w17_classes.json") as json_file:
            w17_classes_config = json.load(json_file)
        # sistema il json di configurazione in modo da avere come chiave primaria
        # id_venue__id_parametro__id_aggregazione__id_time_layouts
        w17_classes_da_inserire = {}  # type: ignore
        for w in w17_classes_config:
            w17_classes_da_inserire[
                HashW17Classes(
                    w17_classes_config[w]["id_parametro"],
                    w17_classes_config[w]["id_time_layouts"],
                    w17_classes_config[w]["id_classes"],
                )
            ] = None
        fine = datetime.datetime.now()
        print(
            "creo i w17_classes vuoti ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        # inserisco tutti i w17_classes
        w17_classes_new_dict = {}
        for w17_classes in w17_classes_da_inserire:
            w17_classes_tmp = w17_classes.split(delimiter)
            my_time_layouts = time_layouts_dict[w17_classes_tmp[1]]
            w17_classes_new_dict[
                HashW17Classes(
                    w17_classes_tmp[0],
                    w17_classes_tmp[1],
                    w17_classes_tmp[2],
                )
            ] = models.W17Classes(
                id_w17=new,
                id_parametro=parametri_dict[w17_classes_tmp[0]],
                id_classes_value=classes_value_dict[
                    str(classes_dict[w17_classes_tmp[2]].id_classes + 80)
                ],  # il valore nullo
                id_classes=classes_dict[w17_classes_tmp[2]],
                id_time_layouts=my_time_layouts,
            )

        # leggo i valori da weather_values per w17_data
        fine = datetime.datetime.now()
        print(
            "inizio carica weather_values per w17_data",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        # variabili necessarie per calcolare il delta tra temp ieri e altroieri
        tmax_altroieri = None
        tmin_altroieri = None
        for w in weather_values_dict:
            w_keys = w.split(delimiter)  # type: ignore
            if (
                HashW17Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                in w17_data_new_dict
            ):
                w17_data_new_dict[
                    HashW17Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                ].numeric_value = weather_values_dict[w].original_numeric_values
                if weather_values_dict[w].original_trend is not None:
                    w17_data_new_dict[
                        HashW17Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                    ].id_trend = weather_values_dict[
                        w
                    ].original_trend.id_trend  # type: ignore
                if "VELR_" in w_keys[1]:
                    w17_data_new_dict[
                        HashW17Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                    ].text_value = weather_values_dict[w].original_text_values
                # se l'original_numeric_values !null e > 0
                if (
                    w17_data_new_dict[
                        HashW17Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                    ].numeric_value
                    is not None
                ):
                    if (
                        w_keys[1] == "PLUV"
                        and (w_keys[2] == "907" or w_keys[2] == "905")
                        and (w_keys[3] == "30" or w_keys[3] == "31")
                    ):
                        # leggi il cod_staz_meteo da original_text_values
                        w17_data_new_dict[
                            HashW17Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                        ].cod_staz_meteo = weather_values_dict[w].original_text_values
                else:
                    # original_numeric_value è NULL
                    if (
                        w_keys[1] == "TERMA"
                        or w_keys[1] == "TERMA_700"
                        or w_keys[1] == "TERMA_1500"
                        or w_keys[1] == "TERMA_2000"
                    ):
                        w17_data_new_dict[
                            HashW17Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                        ].id_trend = (
                            "-1"  # corrisponde al trend n.d. aggiunto lato frontend
                        )
            if (
                w_keys[0] == "67"
                and w_keys[1] == "TERMA"
                and w_keys[2] == "327"
                and w_keys[3] == "17"
            ):
                tmin_altroieri = weather_values_dict[w].original_numeric_values
            if (
                w_keys[0] == "67"
                and w_keys[1] == "TERMA"
                and w_keys[2] == "328"
                and w_keys[3] == "16"
            ):
                tmax_altroieri = weather_values_dict[w].original_numeric_values

        # calcolo di quanto sono incrementate/decrementate tmax e tmin di ieri rispetto al gg prima
        tmin_ieri = w17_data_new_dict[
            HashW17Data("67", "TERMA", "327", "34")
        ].numeric_value
        tmin_diff = tmin_ieri - tmin_altroieri
        if tmin_altroieri is not None and tmin_ieri is not None:
            w17_data_new_dict[HashW17Data("67", "TERMA", "327", "34")].id_trend = (
                tmin_diff
            )
        else:
            w17_data_new_dict[HashW17Data("67", "TERMA", "327", "34")].id_trend = None

        tmax_ieri = w17_data_new_dict[
            HashW17Data("67", "TERMA", "328", "33")
        ].numeric_value
        tmax_diff = tmax_ieri - tmax_altroieri
        if tmax_altroieri is not None and tmax_ieri is not None:
            w17_data_new_dict[HashW17Data("67", "TERMA", "328", "33")].id_trend = (
                tmax_diff
            )
        else:
            w17_data_new_dict[HashW17Data("67", "TERMA", "328", "33")].id_trend = None
        # sistema la velocità del vento tutti i VELR_* diventano VELS e sono tutti accodati
        str_vels = w17_data_new_dict[
            HashW17Data("67", "VELR_700", "0", "32")
        ].text_value
        w17_data_new_dict.pop(HashW17Data("67", "VELR_700", "0", "32"))
        str_vels = (
            str_vels
            + "\n"
            + w17_data_new_dict[HashW17Data("67", "VELR_1500", "0", "32")].text_value
        )
        w17_data_new_dict.pop(HashW17Data("67", "VELR_1500", "0", "32"))
        str_vels = (
            str_vels
            + "\n"
            + w17_data_new_dict[HashW17Data("67", "VELR_2000", "0", "32")].text_value
        )
        w17_data_new_dict.pop(HashW17Data("67", "VELR_2000", "0", "32"))
        w17_data_new_dict[
            HashW17Data(
                w17_data_tmp[0], w17_data_tmp[1], w17_data_tmp[2], w17_data_tmp[3]
            )
        ] = models.W17Data(
            id_w17=new,
            id_venue=venues_dict["67"],
            id_parametro=parametri_dict["VELS"],
            id_aggregazione=aggregazione_dict["912"],
            numeric_value=None,
            id_trend=None,
            text_value=str_vels,
            id_time_layouts=time_layouts_dict["32"],
            cod_staz_meteo=None,
        )
        # salvataggio w17_data
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w17_data ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        w17_data_list = []
        for w in w17_data_new_dict:
            w17_data_list.append(w17_data_new_dict[w])
        #     w17_data_new_dict[w].save()
        models.W17Data.objects.bulk_create(w17_data_list)

        # imposto i valori di default per la localizzazione
        # COP_TOT, id_time_layouts 30 e 31, id_classes a 3
        w17_classes_new_dict[HashW17Classes("COP_TOT", "30", "3")].id_classes_value = (
            classes_value_dict["11"]
        )
        w17_classes_new_dict[HashW17Classes("COP_TOT", "31", "3")].id_classes_value = (
            classes_value_dict["11"]
        )

        # imposto i valori di default per la visibilità presi dal file visibilita_analisi_meteo.json
        if visibilita_ok:
            w17_classes_new_dict[
                HashW17Classes("COP_TOT", "30", "4")
            ].id_classes_value = classes_value_dict[
                visibilita_analisi_meteo["30"]["codice"]
            ]
            w17_classes_new_dict[
                HashW17Classes("COP_TOT", "31", "4")
            ].id_classes_value = classes_value_dict[
                visibilita_analisi_meteo["31"]["codice"]
            ]

        # leggo i valori da weather_values per w17_classes
        fine = datetime.datetime.now()
        print(
            "inizio carica weather_values per w17_classes",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        venues_weather_values = ["171", "172", "173", "174", "175", "176", "177", "178"]
        id_time_layouts_weather_values = ["30", "31"]
        sum = {"30": 0.0, "31": 0.0}
        media_prec_regione = {"30": 0.0, "31": 0.0}
        prec_max_area = {"30": 0.0, "31": 0.0}
        for tl_w in id_time_layouts_weather_values:
            for venue_w in venues_weather_values:
                if weather_values_dict[
                    HashW17Data(
                        venue_w,
                        "PLUV",
                        901,
                        tl_w,
                    )
                ]:
                    original_numeric_values = weather_values_dict[
                        HashW17Data(
                            venue_w,
                            "PLUV",
                            901,
                            tl_w,
                        )
                    ].original_numeric_values
                    if original_numeric_values is not None:
                        sum[tl_w] = sum[tl_w] + float(original_numeric_values)
                        prec_max_area[tl_w] = max(
                            float(original_numeric_values), prec_max_area[tl_w]
                        )
            if sum[tl_w] > 0:
                media_prec_regione[tl_w] = sum[tl_w] / len(venues_weather_values)
        # prec media regione
        w17_classes_new_dict[HashW17Classes("PLUV", "30", "5")].id_classes_value = (
            classes_value_dict[PrecClassMedia(media_prec_regione["30"])]
        )
        w17_classes_new_dict[HashW17Classes("PLUV", "31", "5")].id_classes_value = (
            classes_value_dict[PrecClassMedia(media_prec_regione["31"])]
        )

        # prec max areale
        w17_classes_new_dict[HashW17Classes("PLUV", "30", "6")].id_classes_value = (
            classes_value_dict[PrecClassMaxArea(prec_max_area["30"])]
        )
        w17_classes_new_dict[HashW17Classes("PLUV", "31", "6")].id_classes_value = (
            classes_value_dict[PrecClassMaxArea(prec_max_area["31"])]
        )

        # prec max regione
        prec_max = {"30": 0.0, "31": 0.0}
        for tl_w in id_time_layouts_weather_values:
            for venue_w in venues_weather_values:
                if weather_values_dict[
                    HashW17Data(
                        venue_w,
                        "PLUV",
                        907,
                        tl_w,
                    )
                ]:
                    original_numeric_values = weather_values_dict[
                        HashW17Data(
                            venue_w,
                            "PLUV",
                            907,
                            tl_w,
                        )
                    ].original_numeric_values
                    if original_numeric_values is not None:
                        prec_max[tl_w] = max(
                            float(original_numeric_values), prec_max[tl_w]
                        )
        w17_classes_new_dict[HashW17Classes("PLUV", "30", "7")].id_classes_value = (
            classes_value_dict[PrecClassMax(prec_max["30"])]
        )
        w17_classes_new_dict[HashW17Classes("PLUV", "31", "7")].id_classes_value = (
            classes_value_dict[PrecClassMax(prec_max["31"])]
        )

        # calcolo classi vento
        classe_vento_pianura = None
        valore_vento_pianura = weather_values_dict[
            HashW17Data(
                "67",
                "VELV_700",
                "0",
                "32",
            )
        ].original_numeric_values
        if valore_vento_pianura is not None:
            classe_vento_pianura = WindClassPianura(valore_vento_pianura)
        w17_classes_new_dict[HashW17Classes("VELV", "32", "16")].id_classes_value = (
            classes_value_dict[classe_vento_pianura]
        )

        classe_vento_montagna = None
        valore_vento_montagna = weather_values_dict[
            HashW17Data(
                "67",
                "VELV_2000",
                "0",
                "32",
            )
        ].original_numeric_values
        if valore_vento_montagna is not None:
            classe_vento_montagna = WindClassMontagna(valore_vento_montagna)
        w17_classes_new_dict[HashW17Classes("VELV", "32", "18")].id_classes_value = (
            classes_value_dict[classe_vento_montagna]
        )

        # classes min max TERMA regionale per la verifica
        if tmin_diff > 0:
            tmin_diff_classes_value = 34
        elif tmin_diff == 0:
            tmin_diff_classes_value = 35
        elif tmin_diff < 0:
            tmin_diff_classes_value = 36
        w17_classes_new_dict[HashW17Classes("TERMA", "34", "9")].id_classes_value = (
            classes_value_dict[str(tmin_diff_classes_value)]
        )

        if tmax_diff > 0:
            tmax_diff_classes_value = 37
        elif tmax_diff == 0:
            tmax_diff_classes_value = 38
        elif tmax_diff < 0:
            tmax_diff_classes_value = 39
        w17_classes_new_dict[HashW17Classes("TERMA", "33", "10")].id_classes_value = (
            classes_value_dict[str(tmax_diff_classes_value)]
        )

        # salvataggio w17_classes
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w17_classes ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        w17_classes_list = []
        for ccc in w17_classes_new_dict:
            w17_classes_list.append(w17_classes_new_dict[ccc])
            # w17_classes_new_dict[c].save()
        models.W17Classes.objects.bulk_create(w17_classes_list)

        # salvataggio w17_blob
        w17_blob_list = []
        my_w17_blob = models.W17Blob(
            id_w17=new,
            situation_image=requests.get(url + "/analisi/GEO_0.PNG").content,
            cloudiness_image=requests.get(url + "/analisi/CLOUD_0.PNG").content,
            prec_mattino_image=requests.get(url + "/analisi/PLUV_913.PNG").content,
            prec_pomeriggio_image=requests.get(url + "/analisi/PLUV_914.PNG").content,
            temp_minime_image=requests.get(url + "/analisi/TERMA_327.PNG").content,
            temp_massime_image=requests.get(url + "/analisi/TERMA_328.PNG").content,
        )
        w17_blob_list.append(my_w17_blob)
        models.W17Blob.objects.bulk_create(w17_blob_list)

        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - now).total_seconds()),
            "secondi",
        )

        return Response({"id_w17": new.id_w17})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W17.objects.get(pk=pk)
        print("w17 reopen:", old)
        old.status = "2"
        old_id_w17 = old.id_w17
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w17_parent = old_id_w17
        new.save()
        # print('created: ', new)
        old_data = models.W17Data.objects.filter(id_w17=old_id_w17)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w17 = new
            new_data.save()
        old_classes = models.W17Classes.objects.filter(id_w17=old_id_w17)
        for classs in old_classes:
            new_class = classs
            new_class.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_class.id_w17 = new
            new_class.save()
        old_blobs = models.W17Blob.objects.filter(id_w17=old_id_w17)
        for blob in old_blobs:
            new_blob = blob
            new_blob.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_blob.id_w17 = new
            new_blob.save()

        return Response({"id_w17": new.id_w17})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def copy(self, request, pk):
        # TBD
        return Response({"id_w17": 1})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w17 = models.W17.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w17.id_w17,
            "del",
            w17.data_emissione,
            "iniziato",
        )
        w17.status = "1"
        w17.username = request.user.username
        w17.last_update = inizio
        w17.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("analisi", w17.id_w17)
        return Response({"id_w17": w17.id_w17})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w17/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w17 = snapshots["id_w17"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w17 = models.W17.objects.get(pk=id_w17)
        for snapshot in snapshots:
            setattr(w17, snapshot, snapshots[snapshot])
        w17.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W17SerializerFull(w17, context={"request": request})
        print(
            "bulk_update finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response(
            {
                "updated": updated,
                "last_update": last_update,
                "bulletin": serializer.data,
            }
        )


def convert_to_datetime(d, k):
    d[k] = datetime.datetime.strptime(d[k], "%Y-%m-%d")


def rearrange(time_layout, parametro):
    rearranged = {}
    for v in time_layout[parametro]:
        rearranged[v["id_venue"]] = v
    time_layout[parametro] = rearranged


def rearrange_snow(time_layout, parametro):
    # SNOW_LEV differs for id_aggregation not for the id_venue
    rearranged = {}
    for v in time_layout[parametro]:
        rearranged[v["id_aggregazione"]] = v
    time_layout[parametro] = rearranged


def rearrange_pluv(time_layout, parametro):
    rearranged = {}  # type: ignore

    for z in time_layout[parametro]:
        if z["id_aggregazione"] not in rearranged:
            rearranged[z["id_aggregazione"]] = {}
        if z["id_venue"] in rearranged[z["id_aggregazione"]]:
            rearranged[z["id_aggregazione"]][z["id_venue"]].append(z)
        else:
            rearranged[z["id_aggregazione"]][z["id_venue"]] = [z]

    for v in time_layout[parametro]:
        rearranged[v["id_venue"]] = v
    time_layout[parametro] = rearranged


class W17SVGView(TemplateView):
    template_name = "analisi.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W17.objects
        w17 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W17SerializerFull(w17)
        analisi = serializer.data

        queryset_blob = models.W17Blob.objects
        blob = get_object_or_404(queryset_blob, pk=kwargs["pk"])

        stazione_misura = models_w05.StazioneMisura.objects.exclude(cod_staz_meteo=None)
        stazioni = {}
        for i in stazione_misura:
            k = i.cod_staz_meteo
            if i.quota_sito is not None:
                v = i.denominazione[:14] + " (" + str(round(i.quota_sito)) + "m)"
            stazioni[k] = v

        print("------ blob.situation_image", blob.situation_image)
        if blob.situation_image is not None:
            situation_image = b64encode(blob.situation_image).decode()
        if blob.cloudiness_image is not None:
            cloudiness_image = b64encode(blob.cloudiness_image).decode()
        if blob.prec_mattino_image is not None:
            prec_mattino_image = b64encode(blob.prec_mattino_image).decode()
        if blob.prec_pomeriggio_image is not None:
            prec_pomeriggio_image = b64encode(blob.prec_pomeriggio_image).decode()
        if blob.temp_minime_image is not None:
            temp_minime_image = b64encode(blob.temp_minime_image).decode()
        if blob.temp_massime_image is not None:
            temp_massime_image = b64encode(blob.temp_massime_image).decode()

        convert_to_datetime(analisi, "next_blt_time")
        convert_to_datetime(analisi, "data_emissione")
        convert_to_datetime(analisi, "data_analysis")

        for data in analisi["w17data_set"]:
            if data["id_time_layouts"] not in analisi:
                analisi[data["id_time_layouts"]] = {}
            if data["id_parametro"] in analisi[data["id_time_layouts"]]:
                analisi[data["id_time_layouts"]][data["id_parametro"]].append(data)
            else:
                analisi[data["id_time_layouts"]][data["id_parametro"]] = [data]

        rearrange(analisi[31], "FRZLVL")
        rearrange(analisi[32], "FRZLVL")

        rearrange(analisi[32], "TERMA")
        rearrange(analisi[33], "TERMA")
        rearrange(analisi[34], "TERMA")

        rearrange(analisi[32], "VELS")

        rearrange(analisi[33], "TERMA_700")
        rearrange(analisi[34], "TERMA_700")
        rearrange(analisi[33], "TERMA_1500")
        rearrange(analisi[34], "TERMA_1500")
        rearrange(analisi[33], "TERMA_2000")
        rearrange(analisi[34], "TERMA_2000")

        rearrange_snow(analisi[32], "SNOW_LEV")

        rearrange_pluv(analisi[32], "PLUV")

        rearrange_pluv(analisi[30], "PLUV")
        rearrange_pluv(analisi[31], "PLUV")

        context = {
            "w17": analisi,
            "situation_image": situation_image,
            "cloudiness_image": cloudiness_image,
            "prec_mattino_image": prec_mattino_image,
            "prec_pomeriggio_image": prec_pomeriggio_image,
            "temp_minime_image": temp_minime_image,
            "temp_massime_image": temp_massime_image,
            "stazioni": stazioni,
        }
        return context


class W17PDFView(W17SVGView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="analisi.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response
