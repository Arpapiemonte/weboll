#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import os

import requests

# import tempfile
# from contextlib import closing
# from subprocess import call
from django.contrib.auth.models import User
from django.db.transaction import atomic

# from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# from django.views.generic import DetailView
from django.views.generic.base import TemplateView

# from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from w35.back import models
from w35.back.serializers import (
    AreeMeteoSerializer,
    ForecastComuniSerializer,
    TasksSerializer,
    W35DataSerializer,
    W35Serializer,
    W35SerializerFull,
)

# from w35.back.tasks import refresh_forecast_comuni, save_comuni
from w35.back.tasks import refresh_forecast_comuni
from website.common.tasks import send_with_celery
from website.common.views import (  # ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core import models as models_w05

# from rest_framework_xml.renderers import XMLRenderer
# from wkhtmltopdf.views import PDFTemplateResponse


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W35View(viewsets.ModelViewSet):
    """
    API endpoint that allows W35 bulletins to be viewed or edited
    """

    queryset = models.W35.objects.order_by("-last_update", "-pk")
    serializer_class = W35Serializer
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

    def retrieve(self, request, pk=None):
        queryset = models.W35.objects
        w35 = get_object_or_404(queryset, pk=pk)
        serializer = W35SerializerFull(w35, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W35.objects
        if (
            instance.id_w35_parent
            and queryset.filter(pk=instance.id_w35_parent).exists()
        ):
            w35 = get_object_or_404(queryset, pk=instance.id_w35_parent)
            w35.status = "1"
            if not User.objects.filter(username=w35.username).exists():
                print("perform_destroy non trovo l'utente " + w35.username)
                w35.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w35.save()
        instance.delete()

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w35 = models.W35.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w35.id_w35,
            "del",
            w35.data_emissione,
            "iniziato",
        )
        w35.status = "1"
        w35.username = request.user.username
        w35.last_update = inizio
        w35.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")

        # 873 secs
        # save_comuni.delay(w35.id_w35, request.user.username)
        # send_with_celery("", w35.id_w35)

        # 64 secs
        refresh_forecast_comuni.delay()
        send_with_celery("", w35.id_w35)

        return Response({"id_w35": w35.id_w35})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        delimiter = "__"

        def HashW35Data(id_area_meteo, id_time_layouts, id_parametro):
            return (
                id_area_meteo
                + delimiter
                + str(id_time_layouts)
                + delimiter
                + id_parametro
            )

        w35_data_dict = {}
        id_time_layouts_array = [48, 64, 65, 81, 82, 98, 99]
        id_parametro_array = ["SKY_12", "SNOW_LEV", "ZERO"]

        now = datetime.datetime.now()
        today = datetime.datetime.today()
        today_tostr = today.strftime("%Y%m%d")

        new = models.W35(
            data_emissione=today,
            status="0",  # il nuovo bollettino lo metto in bozza
            last_update=now,
            username=request.user,
        )
        new.save()
        print("created: ", new)

        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for mm in time_layouts:
            time_layouts_dict[mm.id_time_layouts] = mm

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for mmm in sky_conditions:
            sky_conditions_dict[mmm.id_sky_condition] = mmm

        parametro = models.Parametro.objects.all().select_related("id_unita_misura")
        parametro_dict = {}
        for mmmm in parametro:
            parametro_dict[mmmm.id_parametro] = mmmm

        aggregazione = models.Aggregazione.objects.all()
        aggregazione_dict = {}
        for mmmmm in aggregazione:
            aggregazione_dict[mmmmm.id_aggregazione] = mmmmm

        aree_meteo = models.AreeMeteo.objects.all().order_by("id_area")
        aree_meteo_dict = {}
        for mmmmmm in aree_meteo:
            for id_time_layouts in id_time_layouts_array:
                for id_parametro in id_parametro_array:
                    aree_meteo_dict[str(mmmmmm.id_area_meteo)] = mmmmmm
                    numeric_value = None
                    if id_parametro == "SKY_12":
                        numeric_value = 12
                    w35_data_dict[
                        HashW35Data(mmmmmm.id_area_meteo, id_time_layouts, id_parametro)
                    ] = models.W35Data(
                        id_w35=new,
                        id_time_layouts=time_layouts_dict[id_time_layouts],
                        id_area_meteo=mmmmmm,
                        id_parametro=parametro_dict[id_parametro],
                        id_aggregazione=aggregazione_dict[0],
                        numeric_value=numeric_value,
                    )

        # LEGGO METEO
        venue_to_aree_meteo = {
            "89": ["MET-1", "MET-2"],
            "63": ["MET-3"],  # Verbania
            "1": ["MET-4"],  # Biella
            "87": ["MET-5", "MET-6", "MET-8"],  # Cozie
            "88": ["MET-7"],  # Graie
            "90": ["MET-9", "MET-10"],
            "91": ["MET-11"],  # Appennino
            "9": ["MET-12"],  # Alessandria
            "33": ["MET-13"],  # Novara
            "59": ["MET-14", "MET-19"],  # Torino
            "92": ["MET-15"],  # Pianure occidentali
            "28": ["MET-16"],  # Cuneo
            "11": ["MET-17", "MET-18"],  # Asti
        }
        # print(today.date())
        meteo_queryset = models_w05.W05.objects.filter(
            start_valid_time__date=today.date()
        ).filter(status="1")

        url = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")
        url = url + "/w35_json/"

        if meteo_queryset.exists():
            meteo_bulletin = meteo_queryset.get()
            print(
                "prendo gli sky_condition dal bollettino meteo con id "
                + str(meteo_bulletin.id_w05)
            )
            id_w05 = meteo_bulletin.id_w05
            data_meteo_bulletin = models_w05.W05Data.objects.filter(
                id_w05=id_w05
            ).filter(id_parametro="SKY_CONDIT")
            for venue in venue_to_aree_meteo:
                venue_meteo_data = data_meteo_bulletin.filter(id_venue=venue)  # type: ignore
                for area in venue_to_aree_meteo[venue]:
                    for data in venue_meteo_data:
                        w35_data_dict[
                            HashW35Data(
                                area, data.id_time_layouts.id_time_layouts, "SKY_12"
                            )
                        ] = models.W35Data(
                            id_w35=new,
                            id_time_layouts=time_layouts_dict[
                                data.id_time_layouts.id_time_layouts
                            ],
                            id_area_meteo=aree_meteo_dict[area],
                            id_parametro=parametro_dict["SKY_12"],
                            id_aggregazione=aggregazione_dict[0],
                            numeric_value=data.numeric_value,
                        )
        else:
            response = requests.get(url + "w35_sky_cond.json")
            w35_sky_cond = response.json()
            # with open("config/w35_sky_cond.json") as json_file:
            #      w35_sky_cond = json.load(json_file)
            if w35_sky_cond["date"] == today_tostr:
                print("get " + url + "w35_sky_cond.json")
                for data_json in w35_sky_cond["data"]:
                    w35_data_dict[
                        HashW35Data(
                            data_json["id_area_meteo"],
                            data_json["id_time_layouts"],
                            data_json["id_parametro"],
                        )
                    ] = models.W35Data(
                        id_w35=new,
                        id_time_layouts=time_layouts_dict[data_json["id_time_layouts"]],
                        id_area_meteo=aree_meteo_dict[data_json["id_area_meteo"]],
                        id_parametro=parametro_dict[data_json["id_parametro"]],
                        id_aggregazione=aggregazione_dict[0],
                        numeric_value=data_json["numeric_value"],
                    )
            # else:
            #     print("il file w35_sky_cond.json non è aggiornato a oggi")

        response = requests.get(url + "w35_SNOW_LEV.json")
        w35_snow_level = response.json()
        # with open("config/w35_snow_level.json") as json_file:
        #     w35_snow_level = json.load(json_file)

        if w35_snow_level["date"] == today_tostr:
            print("get " + url + "w35_SNOW_LEV.json")
            for data_json in w35_snow_level["data"]:
                w35_data_dict[
                    HashW35Data(
                        data_json["id_area_meteo"],
                        data_json["id_time_layouts"],
                        data_json["id_parametro"],
                    )
                ] = models.W35Data(
                    id_w35=new,
                    id_time_layouts=time_layouts_dict[data_json["id_time_layouts"]],
                    id_area_meteo=aree_meteo_dict[data_json["id_area_meteo"]],
                    id_parametro=parametro_dict[data_json["id_parametro"]],
                    id_aggregazione=aggregazione_dict[0],
                    numeric_value=data_json["numeric_value"],
                )

        response = requests.get(url + "w35_ZERO.json")
        w35_snow_level = response.json()
        # with open("config/w35_ZERO.json") as json_file:
        #     w35_snow_level = json.load(json_file)

        if w35_snow_level["date"] == today_tostr:
            print("get " + url + "w35_ZERO.json")
            for data_json in w35_snow_level["data"]:
                w35_data_dict[
                    HashW35Data(
                        data_json["id_area_meteo"],
                        data_json["id_time_layouts"],
                        data_json["id_parametro"],
                    )
                ] = models.W35Data(
                    id_w35=new,
                    id_time_layouts=time_layouts_dict[data_json["id_time_layouts"]],
                    id_area_meteo=aree_meteo_dict[data_json["id_area_meteo"]],
                    id_parametro=parametro_dict[data_json["id_parametro"]],
                    id_aggregazione=aggregazione_dict[0],
                    numeric_value=data_json["numeric_value"],
                )

        w35_data_save = []
        for w35_data in w35_data_dict:
            w35_data_save.append(w35_data_dict[w35_data])
        models.W35Data.objects.bulk_create(w35_data_save)

        return Response({"id_w35": new.id_w35})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W35.objects.get(pk=pk)
        print("w35 reopen:", old)
        old.status = "2"
        old_id_w35 = old.id_w35
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w35_parent = old_id_w35
        new.save()
        # print('created: ', new)
        old_data = models.W35Data.objects.filter(id_w35=old_id_w35)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w35 = new
            new_data.save()

        return Response({"id_w35": new.id_w35})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w35/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for m in sky_conditions:
            sky_conditions_dict[m.id_sky_condition] = m

        id_w35 = next(s["id"] for s in snapshots if s["id_key"] == "id_w35")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w35",
            "id": id_w35,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w35 = models.W35.objects.get(pk=id_w35)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w35":
                print(
                    "id_w35:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w35, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                print(
                    "id_w35_data:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                data = models.W35Data.objects.get(pk=snapshot["id"])
                setattr(
                    data,
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                data.save()
                updated += 1
        w35.save()
        fine = datetime.datetime.now()
        serializer = W35SerializerFull(w35, context={"request": request})
        print(
            "bulk_update finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response(
            {
                "updated": updated,
                "bulletin": serializer.data,
            }
        )


class W35DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W35 bulletin Data to be viewed or edited
    """

    queryset = models.W35Data.objects.all().order_by("id_w35_data")
    serializer_class = W35DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W35Data.objects
        w35Data = get_object_or_404(queryset, pk=pk)
        serializer = W35DataSerializer(w35Data, context={"request": request})
        return Response(serializer.data)


class HtmlView(TemplateView):
    template_name = "mpa.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W35.objects
        # print("kwargs", kwargs)
        w35 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W35SerializerFull(w35)
        mpa = serializer.data
        context = {
            "mpa": mpa,
        }
        return context


class PdfView(HtmlView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="mpa.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class AreeMeteoView(viewsets.ModelViewSet):
    """
    API endpoint that shows city names
    """

    queryset = models.AreeMeteo.objects.all().order_by("id_area")
    serializer_class = AreeMeteoSerializer
    permission_classes = [ReadOnly]


class TasksView(viewsets.ModelViewSet):
    queryset = models.DjangoCeleryResultsTaskresult.objects.filter(
        task_name="refresh_forecast_comuni"
    ).order_by("-date_created")
    serializer_class = TasksSerializer
    permission_classes = [ReadOnly]


class ForecastComuniView(viewsets.ModelViewSet):
    queryset = models.ForecastComuni.objects.all()

    # https://stackoverflow.com/questions/19707237/use-get-queryset-method-or-set-queryset-variable
    # https://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):
        today = datetime.datetime.today()
        queryset = models.ForecastComuni.objects.all().filter(data_emissione=today)
        return queryset

    serializer_class = ForecastComuniSerializer
    permission_classes = [ReadOnly]
