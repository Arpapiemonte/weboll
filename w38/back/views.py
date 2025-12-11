#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
import os
import tempfile

# from contextlib import closing
from subprocess import call

import requests
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w38.back import models
from w38.back.serializers import (
    W38DataSerializer,
    W38DatiIvreaSerializer,
    W38Serializer,
    W38SerializerFull,
)
from website.common.tasks import send_with_celery
from website.common.views import BulletinDraftLocked, StandardResultsSetPagination
from website.core import models as models_w05


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W38DatiIvreaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W38 DatiI vrea to be viewed
    """

    queryset = models.W38DatiIvrea.objects.all()

    # https://stackoverflow.com/questions/19707237/use-get-queryset-method-or-set-queryset-variable
    # https://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):
        today = datetime.datetime.today()
        queryset = models.W38DatiIvrea.objects.filter(data_emissione=today.date())
        return queryset

    # queryset._result_cache = None
    # print(queryset.count())
    serializer_class = W38DatiIvreaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W38View(viewsets.ModelViewSet):
    """
    API endpoint that allows W38 bulletins to be viewed or edited
    """

    queryset = models.W38.objects.order_by("-last_update", "-pk")
    serializer_class = W38Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        month = self.request.query_params.get("month", "all")
        year = self.request.query_params.get("year", "all")
        order = self.request.query_params.get("order", "-last_update")

        if month != "all":
            queryset = (
                self.get_queryset()
                .filter(data_emissione__year=year)
                .filter(data_emissione__month=month)
                .order_by(order)
            )
        elif year != "all":
            queryset = self.filter_queryset(
                self.get_queryset().filter(data_emissione__year=year).order_by(order)
            )
        else:
            queryset = self.filter_queryset(self.get_queryset().order_by(order))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W38.objects
        if (
            instance.id_w38_parent
            and queryset.filter(pk=instance.id_w38_parent).exists()
        ):
            w38 = get_object_or_404(queryset, pk=instance.id_w38_parent)
            w38.status = "1"
            if not User.objects.filter(username=w38.username).exists():
                print("perform_destroy non trovo l'utente " + w38.username)
                w38.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w38.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W38.objects
        w38 = get_object_or_404(queryset, pk=pk)
        serializer = W38SerializerFull(w38, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W38.objects.get(pk=pk)
        print("w38 reopen:", old)
        old.status = "2"
        old_id_w38 = old.id_w38
        old.save()
        numero_bollettino = int(old.numero_bollettino.split("/")[0])
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.numero_bollettino = (
            str(numero_bollettino) + "/" + str(datetime.datetime.today().year)
        )
        new.last_update = now
        new.username = request.user
        new.id_w38_parent = old_id_w38
        new.save()
        print("created: ", new)
        old_data = models.W38Data.objects.filter(id_w38=old_id_w38)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w38 = new
            new_data.save()

        return Response({"id_w38": new.id_w38})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w38 = models.W38.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w38.id_w38,
            "del",
            w38.data_emissione,
            "iniziato",
        )
        w38.status = "1"
        w38.username = request.user.username
        w38.last_update = inizio
        w38.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("uvi", w38.id_w38)
        return Response({"id_w38": w38.id_w38})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):

        # delimiter_firstguess = ";"
        delimiter = "__"

        def HashW38Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
            return (
                str(id_venue)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(id_time_layouts)
            )

        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today

        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = emissione + datetime.timedelta(days=1)

        create_empty = False
        if (
            not models.W38.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            numero_bollettino = 1
            print(
                "new del bollettino ",
                numero_bollettino,
                "del",
                today,
                "iniziato",
            )
        else:
            old_w38 = (
                models.W38.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
            print(
                "new del bollettino ",
                old_w38.id_w38,
                "del",
                old_w38.data_emissione,
                "iniziato",
            )

            # aumento il sequenziale perchè è una nuova emissione
            numero_bollettino = int(old_w38.numero_bollettino.split("/")[0])
            numero_bollettino = numero_bollettino + 1
            print(numero_bollettino, old_w38.data_emissione.year)
            # gestione anno nuovo
            if old_w38.data_emissione.year < today.year:
                print("new(): cambio dell'anno imposto il sequenziale a 1")
                numero_bollettino = 1

        if create_empty:
            situazione_evoluzione = ""
            note = "-"
        else:
            situazione_evoluzione = str(old_w38.situazione_evoluzione)
            note = "-"
        # gestione situazione_evoluzione ultimo bol meteo

        latest_w05 = models_w05.W05.objects.filter(status="1").order_by("-last_update")
        if latest_w05:
            situazione_evoluzione = str(latest_w05[0].situation)
        else:
            situazione_evoluzione = ""

        new = models.W38(
            data_emissione=emissione.date(),
            data_validita=tomorrow.date(),
            situazione_evoluzione=situazione_evoluzione,
            note=note,
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            numero_bollettino=str(numero_bollettino) + "/" + str(today.year),
        )
        new.save()
        # carico la configurazione json per sapere quanti record ci devono essere su w05_data
        with open("config/w38_data.json") as json_file:
            w38_data_config = json.load(json_file)

            time_layouts = models_w05.TimeLayouts.objects.all()
            time_layouts_dict = {}
            for t in time_layouts:
                time_layouts_dict[str(t.id_time_layouts)] = t

            aggregazione = models_w05.Aggregazione.objects.all().order_by(
                "id_aggregazione"
            )
            aggregazione_dict = {}
            for a in aggregazione:
                aggregazione_dict[str(a.id_aggregazione)] = a

            parametri = models_w05.Parametro.objects.all()
            parametri_dict = {}
            for p in parametri:
                parametri_dict[p.id_parametro] = p

        w38_data_new_dict = {}
        for w38 in w38_data_config:
            w38_data_new_dict[
                HashW38Data(
                    w38["id_venue"],
                    w38["id_parametro"],
                    w38["id_aggregazione"],
                    w38["id_time_layouts"],
                )
            ] = models.W38Data(
                id_w38=new,
                id_venue=int(w38["id_venue"]),
                id_parametro=parametri_dict[w38["id_parametro"]],
                id_aggregazione=aggregazione_dict[str(w38["id_aggregazione"])],
                id_time_layouts=time_layouts_dict[str(w38["id_time_layouts"])],
                # numeric_value=None,
                numeric_value="1",
            )
        try:
            # ricerca della data di emmissione più recente
            # data_emiss_query = models.W38DatiIvrea.objects.order_by(
            #     "-data_emissione"
            # ).latest("pk")
            # ricerca della penultima data di emmissione più recente
            data_oggi_esiste = models.W38DatiIvrea.objects.filter(
                data_emissione=today.date()
            ).exists()
            print("data_oggi_esiste=", data_oggi_esiste)
            if data_oggi_esiste:
                print("data_oggi_esiste=", data_oggi_esiste)
                uvi_data_ivrea = models.W38DatiIvrea.objects.filter(
                    data_emissione=today.date()
                )
                for feature in uvi_data_ivrea:
                    w38_data_new_dict[
                        HashW38Data(
                            feature.id_venue,
                            "UVICS",
                            "0",
                            str(feature.id_time_layouts.id_time_layouts),
                        )
                    ] = models.W38Data(  # type: ignore
                        id_w38=new,
                        id_venue=feature.id_venue,
                        id_parametro=parametri_dict["UVICS"],
                        id_aggregazione=aggregazione_dict["0"],
                        id_time_layouts=time_layouts_dict[
                            str(feature.id_time_layouts.id_time_layouts)
                        ],
                        # numeric_value="2",
                        numeric_value=int(feature.numeric_value),  # type: ignore
                    )
            else:
                print("data_oggi_non_esiste=", data_oggi_esiste)
                old_w38 = (
                    models.W38.objects.filter(status="1")
                    .order_by("-last_update")
                    .latest("pk")
                )
                print(old_w38.id_w38)
                uvi_data_ivrea = models.W38Data.objects.filter(
                    id_w38=int(old_w38.id_w38)
                )  # type: ignore
                # print("uvi_data_ivrea=",uvi_data_ivrea)
                for feature in uvi_data_ivrea:
                    # print('------',str(feature.id_parametro.id_parametro))
                    if str(feature.id_parametro.id_parametro) == "UVICS":  # type: ignore
                        # print('feature.id_venue',feature.id_venue)
                        # print('------',str(feature.id_time_layouts.id_time_layouts))
                        # print('------',feature.id_time_layouts.id_time_layouts)
                        # print('------',feature.numeric_value)
                        w38_data_new_dict[
                            HashW38Data(
                                feature.id_venue,
                                "UVICS",
                                "0",
                                str(feature.id_time_layouts.id_time_layouts),
                            )
                        ] = models.W38Data(  # type: ignore
                            id_w38=new,
                            id_venue=feature.id_venue,
                            id_parametro=parametri_dict["UVICS"],
                            id_aggregazione=aggregazione_dict["0"],
                            id_time_layouts=time_layouts_dict[
                                str(feature.id_time_layouts.id_time_layouts)
                            ],
                            # numeric_value="2",
                            numeric_value=int(feature.numeric_value),  # type: ignore
                        )
        except Exception:
            pass
            print("dat uvi Ivrea per oggi o ieri non esistono non li trovo")
        try:
            urlcop = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")
            urlcop += "/uvi/" + today.strftime("%Y%m%d") + "_cop_tot.json"
            # urlcop += "/uvi/yyyymmgg_cop_tot.json"
            print("url", urlcop)
            uvi_firstguescop = json.loads(requests.get(urlcop).content)
            for feature in uvi_firstguescop:
                w38_data_new_dict[
                    HashW38Data(
                        feature["id_venue"],  # type: ignore
                        feature["id_parametro"],  # type: ignore
                        feature["id_aggregazione"],  # type: ignore
                        feature["id_time_layouts"],  # type: ignore
                    )
                ] = models.W38Data(
                    id_w38=new,
                    id_venue=int(feature["id_venue"]),  # type: ignore
                    id_parametro=parametri_dict[feature["id_parametro"]],  # type: ignore
                    id_aggregazione=aggregazione_dict[str(feature["id_aggregazione"])],  # type: ignore
                    id_time_layouts=time_layouts_dict[str(feature["id_time_layouts"])],  # type: ignore
                    # numeric_value=None,
                    numeric_value=feature["numeric_values"],  # type: ignore
                )
            print("uvi_data_ivrea2", w38_data_new_dict["1__COP_TOT__0__48"])
        except Exception:
            pass
            print("url previsioni copertura non esiste non la trovo")
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w38_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w38_data_list = []
        for w38d in w38_data_new_dict:
            # if type(w38_data_new_dict[w38d]) is models_w05.WeatherValues:
            w38_data_record = models.W38Data(
                id_w38=new,
                id_venue=w38_data_new_dict[w38d].id_venue,
                id_parametro=w38_data_new_dict[w38d].id_parametro,
                id_aggregazione=w38_data_new_dict[w38d].id_aggregazione,
                id_time_layouts=w38_data_new_dict[w38d].id_time_layouts,
                numeric_value=w38_data_new_dict[w38d].numeric_value,
            )
            w38_data_list.append(w38_data_record)
        models.W38Data.objects.bulk_create(w38_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w38": new.id_w38})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w38/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w38 = snapshots["id_w38"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w38 = models.W38.objects.get(pk=id_w38)
        for snapshot in snapshots:
            setattr(w38, snapshot, snapshots[snapshot])
        w38.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W38SerializerFull(w38, context={"request": request})
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


class W38DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W38 bulletin Data to be viewed or edited
    """

    queryset = models.W38Data.objects.all()
    serializer_class = W38DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W38Data.objects
        w38Data = get_object_or_404(queryset, pk=pk)
        serializer = W38DataSerializer(w38Data, context={"request": request})
        return Response(serializer.data)


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


class UviHTMLView(TemplateView):
    template_name = "uvi.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W38.objects
        w38 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W38SerializerFull(w38)
        uvi = serializer.data
        uvi_rearranged = {}  # type: ignore
        # uvi_calc_rearranged = {}  # type: ignore
        for data in uvi["w38data_set"]:
            if data["id_venue"] not in uvi_rearranged:
                uvi_rearranged[data["id_venue"]] = {}
            if data["id_parametro"] not in uvi_rearranged[data["id_venue"]]:
                uvi_rearranged[data["id_venue"]][data["id_parametro"]] = {}
            if (
                data["id_aggregazione"]
                not in uvi_rearranged[data["id_venue"]][data["id_parametro"]]
            ):
                uvi_rearranged[data["id_venue"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ] = {}
            if (
                data["id_time_layouts"]
                not in uvi_rearranged[data["id_venue"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ]
            ):
                uvi_rearranged[data["id_venue"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ][data["id_time_layouts"]] = {}
            uvi_rearranged[data["id_venue"]][data["id_parametro"]][
                data["id_aggregazione"]
            ][data["id_time_layouts"]] = float((data["numeric_value"]))

        uvi_rearrangedint = {}  # type: ignore
        # uvi_calc_rearranged = {}  # type: ignore
        for data in uvi["w38data_set"]:
            if data["id_venue"] not in uvi_rearrangedint:
                uvi_rearrangedint[data["id_venue"]] = {}
            if data["id_parametro"] not in uvi_rearrangedint[data["id_venue"]]:
                uvi_rearrangedint[data["id_venue"]][data["id_parametro"]] = {}
            if (
                data["id_aggregazione"]
                not in uvi_rearrangedint[data["id_venue"]][data["id_parametro"]]
            ):
                uvi_rearrangedint[data["id_venue"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ] = {}
            if (
                data["id_time_layouts"]
                not in uvi_rearrangedint[data["id_venue"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ]
            ):
                uvi_rearrangedint[data["id_venue"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ][data["id_time_layouts"]] = {}
            uvi_rearrangedint[data["id_venue"]][data["id_parametro"]][
                data["id_aggregazione"]
            ][data["id_time_layouts"]] = int((data["numeric_value"]))

        uvics_data = {}
        uvicl_data = {}
        for key, value in uvi_rearranged.items():
            if "UVICS" in value:
                uvics_data[key] = value["UVICS"]
            if "COP_TOT" in value:
                uvicl_data[key] = value["COP_TOT"]
        uvi_rearranged_calc = {
            9: {},
            11: {},
            1: {},
            28: {},
            33: {},
            59: {},
            63: {},
            64: {},
            89: {},
            190: {},
            88: {},
            87: {},
            90: {},
            116: {},
            91: {},
            191: {},
            192: {},
            16: {},
        }  # type: ignore
        # 9 Alessandria
        uvi_rearranged_calc[9][48] = int(
            round(uvics_data["9"][0][48] * uvicl_data["9"][0][48])
        )
        if uvi_rearranged_calc[9][48] > 11:
            uvi_rearranged_calc[9][48] = 11
        if uvi_rearranged_calc[9][48] < 1:
            uvi_rearranged_calc[9][48] = 1
        uvi_rearranged_calc[9][66] = int(
            round(uvics_data["9"][0][66] * uvicl_data["9"][0][66])
        )
        if uvi_rearranged_calc[9][66] > 11:
            uvi_rearranged_calc[9][66] = 11
        if uvi_rearranged_calc[9][66] < 1:
            uvi_rearranged_calc[9][66] = 1
        uvi_rearranged_calc[9][83] = int(
            round(uvics_data["9"][0][83] * uvicl_data["9"][0][83])
        )
        if uvi_rearranged_calc[9][83] > 11:
            uvi_rearranged_calc[9][83] = 11
        if uvi_rearranged_calc[9][83] < 1:
            uvi_rearranged_calc[9][83] = 1
        # 11 Asti
        uvi_rearranged_calc[11][48] = int(
            round(uvics_data["11"][0][48] * uvicl_data["11"][0][48])
        )
        if uvi_rearranged_calc[11][48] > 11:
            uvi_rearranged_calc[11][48] = 11
        if uvi_rearranged_calc[11][48] < 1:
            uvi_rearranged_calc[11][48] = 1
        uvi_rearranged_calc[11][66] = int(
            round(uvics_data["11"][0][66] * uvicl_data["11"][0][66])
        )
        if uvi_rearranged_calc[11][66] > 11:
            uvi_rearranged_calc[11][66] = 11
        if uvi_rearranged_calc[11][66] < 1:
            uvi_rearranged_calc[11][66] = 1
        uvi_rearranged_calc[11][83] = int(
            round(uvics_data["11"][0][83] * uvicl_data["11"][0][83])
        )
        if uvi_rearranged_calc[11][83] > 11:
            uvi_rearranged_calc[11][83] = 11
        if uvi_rearranged_calc[11][83] < 1:
            uvi_rearranged_calc[11][83] = 1
        # 1 Biella
        uvi_rearranged_calc[1][48] = int(
            round(uvics_data["1"][0][48] * uvicl_data["1"][0][48])
        )
        if uvi_rearranged_calc[1][48] > 11:
            uvi_rearranged_calc[1][48] = 11
        if uvi_rearranged_calc[1][48] < 1:
            uvi_rearranged_calc[1][48] = 1
        uvi_rearranged_calc[1][66] = int(
            round(uvics_data["1"][0][66] * uvicl_data["1"][0][66])
        )
        if uvi_rearranged_calc[1][66] > 11:
            uvi_rearranged_calc[1][66] = 11
        if uvi_rearranged_calc[1][66] < 1:
            uvi_rearranged_calc[1][66] = 1
        uvi_rearranged_calc[1][83] = int(
            round(uvics_data["1"][0][83] * uvicl_data["1"][0][83])
        )
        if uvi_rearranged_calc[1][83] > 11:
            uvi_rearranged_calc[1][83] = 11
        if uvi_rearranged_calc[1][83] < 1:
            uvi_rearranged_calc[1][83] = 1
        # 28 Cuneo
        uvi_rearranged_calc[28][48] = int(
            round(uvics_data["28"][0][48] * uvicl_data["28"][0][48])
        )
        if uvi_rearranged_calc[28][48] > 11:
            uvi_rearranged_calc[28][48] = 11
        if uvi_rearranged_calc[28][48] < 1:
            uvi_rearranged_calc[28][48] = 1
        uvi_rearranged_calc[28][66] = int(
            round(uvics_data["28"][0][66] * uvicl_data["28"][0][66])
        )
        if uvi_rearranged_calc[28][66] > 11:
            uvi_rearranged_calc[28][66] = 11
        if uvi_rearranged_calc[28][66] < 1:
            uvi_rearranged_calc[28][66] = 1
        uvi_rearranged_calc[28][83] = int(
            round(uvics_data["28"][0][83] * uvicl_data["28"][0][83])
        )
        if uvi_rearranged_calc[28][83] > 11:
            uvi_rearranged_calc[28][83] = 11
        if uvi_rearranged_calc[28][83] < 1:
            uvi_rearranged_calc[28][83] = 1
        # 33 Novara
        uvi_rearranged_calc[33][48] = int(
            round(uvics_data["33"][0][48] * uvicl_data["33"][0][48])
        )
        if uvi_rearranged_calc[33][48] > 11:
            uvi_rearranged_calc[33][48] = 11
        if uvi_rearranged_calc[33][48] < 1:
            uvi_rearranged_calc[33][48] = 1
        uvi_rearranged_calc[33][66] = int(
            round(uvics_data["33"][0][66] * uvicl_data["33"][0][66])
        )
        if uvi_rearranged_calc[33][66] > 11:
            uvi_rearranged_calc[33][66] = 11
        if uvi_rearranged_calc[33][66] < 1:
            uvi_rearranged_calc[33][66] = 1
        uvi_rearranged_calc[33][83] = int(
            round(uvics_data["33"][0][83] * uvicl_data["33"][0][83])
        )
        if uvi_rearranged_calc[33][83] > 11:
            uvi_rearranged_calc[33][83] = 11
        if uvi_rearranged_calc[33][83] < 1:
            uvi_rearranged_calc[33][83] = 1
        # 59 Torino
        uvi_rearranged_calc[59][48] = int(
            round(uvics_data["59"][0][48] * uvicl_data["59"][0][48])
        )
        if uvi_rearranged_calc[59][48] > 11:
            uvi_rearranged_calc[59][48] = 11
        if uvi_rearranged_calc[59][48] < 1:
            uvi_rearranged_calc[59][48] = 1
        uvi_rearranged_calc[59][66] = int(
            round(uvics_data["59"][0][66] * uvicl_data["59"][0][66])
        )
        if uvi_rearranged_calc[59][66] > 11:
            uvi_rearranged_calc[59][66] = 11
        if uvi_rearranged_calc[59][66] < 1:
            uvi_rearranged_calc[59][66] = 1
        uvi_rearranged_calc[59][83] = int(
            round(uvics_data["59"][0][83] * uvicl_data["59"][0][83])
        )
        if uvi_rearranged_calc[59][83] > 11:
            uvi_rearranged_calc[59][83] = 11
        if uvi_rearranged_calc[59][83] < 1:
            uvi_rearranged_calc[59][83] = 1
        # 63 Verbania
        uvi_rearranged_calc[63][48] = int(
            round(uvics_data["63"][0][48] * uvicl_data["63"][0][48])
        )
        if uvi_rearranged_calc[63][48] > 11:
            uvi_rearranged_calc[63][48] = 11
        if uvi_rearranged_calc[63][48] < 1:
            uvi_rearranged_calc[63][48] = 1
        uvi_rearranged_calc[63][66] = int(
            round(uvics_data["63"][0][66] * uvicl_data["63"][0][66])
        )
        if uvi_rearranged_calc[63][66] > 11:
            uvi_rearranged_calc[63][66] = 11
        if uvi_rearranged_calc[63][66] < 1:
            uvi_rearranged_calc[63][66] = 1
        uvi_rearranged_calc[63][83] = int(
            round(uvics_data["63"][0][83] * uvicl_data["63"][0][83])
        )
        if uvi_rearranged_calc[63][83] > 11:
            uvi_rearranged_calc[63][83] = 11
        if uvi_rearranged_calc[63][83] < 1:
            uvi_rearranged_calc[63][83] = 1
        # 64 Vercelli
        uvi_rearranged_calc[64][48] = int(
            round(uvics_data["64"][0][48] * uvicl_data["64"][0][48])
        )
        if uvi_rearranged_calc[64][48] > 11:
            uvi_rearranged_calc[64][48] = 11
        if uvi_rearranged_calc[64][48] < 1:
            uvi_rearranged_calc[64][48] = 1
        uvi_rearranged_calc[64][66] = int(
            round(uvics_data["64"][0][66] * uvicl_data["64"][0][66])
        )
        if uvi_rearranged_calc[64][66] > 11:
            uvi_rearranged_calc[64][66] = 11
        if uvi_rearranged_calc[64][66] < 1:
            uvi_rearranged_calc[64][66] = 1
        uvi_rearranged_calc[64][83] = int(
            round(uvics_data["64"][0][83] * uvicl_data["64"][0][83])
        )
        if uvi_rearranged_calc[64][83] > 11:
            uvi_rearranged_calc[64][83] = 11
        if uvi_rearranged_calc[64][83] < 1:
            uvi_rearranged_calc[64][83] = 1
        # 89 Alpi Lepontine
        uvi_rearranged_calc[89][48] = int(
            round(uvics_data["89"][0][48] * uvicl_data["89"][0][48])
        )
        if uvi_rearranged_calc[89][48] > 11:
            uvi_rearranged_calc[89][48] = 11
        if uvi_rearranged_calc[89][48] < 1:
            uvi_rearranged_calc[89][48] = 1
        uvi_rearranged_calc[89][66] = int(
            round(uvics_data["89"][0][66] * uvicl_data["89"][0][66])
        )
        if uvi_rearranged_calc[89][66] > 11:
            uvi_rearranged_calc[89][66] = 11
        if uvi_rearranged_calc[89][66] < 1:
            uvi_rearranged_calc[89][66] = 1
        uvi_rearranged_calc[89][83] = int(
            round(uvics_data["89"][0][83] * uvicl_data["89"][0][83])
        )
        if uvi_rearranged_calc[89][83] > 11:
            uvi_rearranged_calc[89][83] = 11
        if uvi_rearranged_calc[89][83] < 1:
            uvi_rearranged_calc[89][83] = 1
        # 190 Alpi Pennine
        uvi_rearranged_calc[190][48] = int(
            round(uvics_data["190"][0][48] * uvicl_data["190"][0][48])
        )
        if uvi_rearranged_calc[190][48] > 11:
            uvi_rearranged_calc[190][48] = 11
        if uvi_rearranged_calc[190][48] < 1:
            uvi_rearranged_calc[190][48] = 1
        uvi_rearranged_calc[190][66] = int(
            round(uvics_data["190"][0][66] * uvicl_data["190"][0][66])
        )
        if uvi_rearranged_calc[190][66] > 11:
            uvi_rearranged_calc[190][66] = 11
        if uvi_rearranged_calc[190][66] < 1:
            uvi_rearranged_calc[190][66] = 1
        uvi_rearranged_calc[190][83] = int(
            round(uvics_data["190"][0][83] * uvicl_data["190"][0][83])
        )
        if uvi_rearranged_calc[190][83] > 11:
            uvi_rearranged_calc[190][83] = 11
        if uvi_rearranged_calc[190][83] < 1:
            uvi_rearranged_calc[190][83] = 1
        # 88 Alpi Graie
        uvi_rearranged_calc[88][48] = int(
            round(uvics_data["88"][0][48] * uvicl_data["88"][0][48])
        )
        if uvi_rearranged_calc[88][48] > 11:
            uvi_rearranged_calc[88][48] = 11
        if uvi_rearranged_calc[88][48] < 1:
            uvi_rearranged_calc[88][48] = 1
        uvi_rearranged_calc[88][66] = int(
            round(uvics_data["88"][0][66] * uvicl_data["88"][0][66])
        )
        if uvi_rearranged_calc[88][66] > 11:
            uvi_rearranged_calc[88][66] = 11
        if uvi_rearranged_calc[88][66] < 1:
            uvi_rearranged_calc[88][66] = 1
        uvi_rearranged_calc[88][83] = int(
            round(uvics_data["88"][0][83] * uvicl_data["88"][0][83])
        )
        if uvi_rearranged_calc[88][83] > 11:
            uvi_rearranged_calc[88][83] = 11
        if uvi_rearranged_calc[88][83] < 1:
            uvi_rearranged_calc[88][83] = 1
        # 87 Alpi Cozie
        uvi_rearranged_calc[87][48] = int(
            round(uvics_data["87"][0][48] * uvicl_data["87"][0][48])
        )
        if uvi_rearranged_calc[87][48] > 11:
            uvi_rearranged_calc[87][48] = 11
        if uvi_rearranged_calc[87][48] < 1:
            uvi_rearranged_calc[87][48] = 1
        uvi_rearranged_calc[87][66] = int(
            round(uvics_data["87"][0][66] * uvicl_data["87"][0][66])
        )
        if uvi_rearranged_calc[87][66] > 11:
            uvi_rearranged_calc[87][66] = 11
        if uvi_rearranged_calc[87][66] < 1:
            uvi_rearranged_calc[87][66] = 1
        uvi_rearranged_calc[87][83] = int(
            round(uvics_data["87"][0][83] * uvicl_data["87"][0][83])
        )
        if uvi_rearranged_calc[87][83] > 11:
            uvi_rearranged_calc[87][83] = 11
        if uvi_rearranged_calc[87][83] < 1:
            uvi_rearranged_calc[87][83] = 1
        # 90 Alpi Marittime
        uvi_rearranged_calc[90][48] = int(
            round(uvics_data["90"][0][48] * uvicl_data["90"][0][48])
        )
        if uvi_rearranged_calc[90][48] > 11:
            uvi_rearranged_calc[90][48] = 11
        if uvi_rearranged_calc[90][48] < 1:
            uvi_rearranged_calc[90][48] = 1
        uvi_rearranged_calc[90][66] = int(
            round(uvics_data["90"][0][66] * uvicl_data["90"][0][66])
        )
        if uvi_rearranged_calc[90][66] > 11:
            uvi_rearranged_calc[90][66] = 11
        if uvi_rearranged_calc[90][66] < 1:
            uvi_rearranged_calc[90][66] = 1
        uvi_rearranged_calc[90][83] = int(
            round(uvics_data["90"][0][83] * uvicl_data["90"][0][83])
        )
        if uvi_rearranged_calc[90][83] > 11:
            uvi_rearranged_calc[90][83] = 11
        if uvi_rearranged_calc[90][83] < 1:
            uvi_rearranged_calc[90][83] = 1
        # 116 Alpi Liguri
        uvi_rearranged_calc[116][48] = int(
            round(uvics_data["116"][0][48] * uvicl_data["116"][0][48])
        )
        if uvi_rearranged_calc[116][48] > 11:
            uvi_rearranged_calc[116][48] = 11
        if uvi_rearranged_calc[116][48] < 1:
            uvi_rearranged_calc[116][48] = 1
        uvi_rearranged_calc[116][66] = int(
            round(uvics_data["116"][0][66] * uvicl_data["116"][0][66])
        )
        if uvi_rearranged_calc[116][66] > 11:
            uvi_rearranged_calc[116][66] = 11
        if uvi_rearranged_calc[116][66] < 1:
            uvi_rearranged_calc[116][66] = 1
        uvi_rearranged_calc[116][83] = int(
            round(uvics_data["116"][0][83] * uvicl_data["116"][0][83])
        )
        if uvi_rearranged_calc[116][83] > 11:
            uvi_rearranged_calc[116][83] = 11
        if uvi_rearranged_calc[116][83] < 1:
            uvi_rearranged_calc[116][83] = 1
        # 91 Appennino
        uvi_rearranged_calc[91][48] = int(
            round(uvics_data["91"][0][48] * uvicl_data["91"][0][48])
        )
        if uvi_rearranged_calc[91][48] > 11:
            uvi_rearranged_calc[91][48] = 11
        if uvi_rearranged_calc[91][48] < 1:
            uvi_rearranged_calc[91][48] = 1
        uvi_rearranged_calc[91][66] = int(
            round(uvics_data["91"][0][66] * uvicl_data["91"][0][66])
        )
        if uvi_rearranged_calc[91][66] > 11:
            uvi_rearranged_calc[91][66] = 11
        if uvi_rearranged_calc[91][66] < 1:
            uvi_rearranged_calc[91][66] = 1
        uvi_rearranged_calc[91][83] = int(
            round(uvics_data["91"][0][83] * uvicl_data["91"][0][83])
        )
        if uvi_rearranged_calc[91][83] > 11:
            uvi_rearranged_calc[91][83] = 11
        if uvi_rearranged_calc[91][83] < 1:
            uvi_rearranged_calc[91][83] = 1
        # 191 Lago Orta
        uvi_rearranged_calc[191][48] = int(
            round(uvics_data["191"][0][48] * uvicl_data["191"][0][48])
        )
        if uvi_rearranged_calc[191][48] > 11:
            uvi_rearranged_calc[191][48] = 11
        if uvi_rearranged_calc[191][48] < 1:
            uvi_rearranged_calc[191][48] = 1
        uvi_rearranged_calc[191][66] = int(
            round(uvics_data["191"][0][66] * uvicl_data["191"][0][66])
        )
        if uvi_rearranged_calc[191][66] > 11:
            uvi_rearranged_calc[191][66] = 11
        if uvi_rearranged_calc[191][66] < 1:
            uvi_rearranged_calc[191][66] = 1
        uvi_rearranged_calc[191][83] = int(
            round(uvics_data["191"][0][83] * uvicl_data["191"][0][83])
        )
        if uvi_rearranged_calc[191][83] > 11:
            uvi_rearranged_calc[191][83] = 11
        if uvi_rearranged_calc[191][83] < 1:
            uvi_rearranged_calc[191][83] = 1
        # 192 Lago Avigliana
        uvi_rearranged_calc[192][48] = int(
            round(uvics_data["192"][0][48] * uvicl_data["192"][0][48])
        )
        if uvi_rearranged_calc[192][48] > 11:
            uvi_rearranged_calc[192][48] = 11
        if uvi_rearranged_calc[192][48] < 1:
            uvi_rearranged_calc[192][48] = 1
        print("avigliana oggi", uvi_rearranged_calc[192][48])
        print("avigliana oggi ", uvics_data["192"][0][48])
        print("avigliana oggi ", uvicl_data["192"][0][48])
        uvi_rearranged_calc[192][66] = int(
            round(uvics_data["192"][0][66] * uvicl_data["192"][0][66])
        )
        if uvi_rearranged_calc[192][66] > 11:
            uvi_rearranged_calc[192][66] = 11
        if uvi_rearranged_calc[192][66] < 1:
            uvi_rearranged_calc[192][66] = 1
        print("avigliana domani", uvi_rearranged_calc[192][66])
        uvi_rearranged_calc[192][83] = int(
            round(uvics_data["192"][0][83] * uvicl_data["192"][0][83])
        )
        if uvi_rearranged_calc[192][83] > 11:
            uvi_rearranged_calc[192][83] = 11
        if uvi_rearranged_calc[192][83] < 1:
            uvi_rearranged_calc[192][83] = 1
        print("avigliana dopo domani", uvi_rearranged_calc[192][83])
        # 16 Lago sirio Ivrea
        uvi_rearranged_calc[16][48] = int(
            round(uvics_data["16"][0][48] * uvicl_data["16"][0][48])
        )
        if uvi_rearranged_calc[16][48] > 11:
            uvi_rearranged_calc[16][48] = 11
        if uvi_rearranged_calc[16][48] < 1:
            uvi_rearranged_calc[16][48] = 1
        uvi_rearranged_calc[16][66] = int(
            round(uvics_data["16"][0][66] * uvicl_data["16"][0][66])
        )
        if uvi_rearranged_calc[16][66] > 11:
            uvi_rearranged_calc[16][66] = 11
        if uvi_rearranged_calc[16][66] < 1:
            uvi_rearranged_calc[16][66] = 1
        uvi_rearranged_calc[16][83] = int(
            round(uvics_data["16"][0][83] * uvicl_data["16"][0][83])
        )
        if uvi_rearranged_calc[16][83] > 11:
            uvi_rearranged_calc[16][83] = 11
        if uvi_rearranged_calc[16][83] < 1:
            uvi_rearranged_calc[16][83] = 1

        # (uvi_rearranged_calc)
        convert_to_date(uvi, "data_validita")
        convert_to_date(uvi, "data_emissione")

        context = {
            "uvi": uvi,
            "title": "Bollettino Uvi",
            "uvi_arra": uvi_rearrangedint,
            "uvi_rearranged_calc": uvi_rearranged_calc,
        }
        return context


class UviPDFView(UviHTMLView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="uvi.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class UviPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        django_url = os.getenv("DJANGO_URL", "http://django:8000")
        r = requests.get(django_url + "/w38/pdf/%d" % kwargs["pk"])

        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(r.content)
            f.flush()
            png_name = "%s.png" % f.name
            command = "convert -verbose -density 145 -crop 1191x1685+3x5 %s %s" % (
                f.name,
                png_name,
            )
            retcode = call(command, shell=True)
            if retcode != 0:
                error = "imagemagick convert failed with code: %d" % retcode
                raise Exception(error)
            with open(png_name, mode="rb") as png_file:
                png_content = png_file.read()
            os.remove(png_name)
            return HttpResponse(
                content=memoryview(png_content), content_type="image/png"
            )
