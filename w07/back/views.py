#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
import os

# import tempfile
# from contextlib import closing
# from subprocess import call
# import requests
from decimal import Decimal

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

# from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w07.back import models
from w07.back.serializers import W07DataSerializer, W07Serializer, W07SerializerFull
from w33.back import models as w33models
from website.common.tasks import send_with_celery
from website.common.views import (  # ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core import models as websitecoremodels


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W07View(viewsets.ModelViewSet):
    """
    API endpoint that allows W07 bulletins to be viewed or edited
    """

    queryset = models.W07.objects.order_by("-last_update", "-pk")
    serializer_class = W07Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        month = self.request.query_params.get("month", "all")
        year = self.request.query_params.get("year", "all")
        order = self.request.query_params.get("order", "-last_update")

        if month != "all":
            queryset = (
                self.get_queryset()
                .filter(start_valid_time__year=year)
                .filter(start_valid_time__month=month)
                .order_by(order)
            )
        elif year != "all":
            queryset = self.filter_queryset(
                self.get_queryset().filter(start_valid_time__year=year).order_by(order)
            )
        else:
            queryset = self.filter_queryset(self.get_queryset().order_by(order))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = models.W07.objects
        w07 = get_object_or_404(queryset, pk=pk)
        serializer = W07SerializerFull(w07, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W07.objects
        if (
            instance.id_w07_parent
            and queryset.filter(pk=instance.id_w07_parent).exists()
        ):
            w07 = get_object_or_404(queryset, pk=instance.id_w07_parent)
            w07.status = "1"
            if not User.objects.filter(username=w07.username).exists():
                print("perform_destroy non trovo l'utente " + w07.username)
                w07.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w07.save()
        instance.delete()

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w07 = models.W07.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w07.id_w07,
            "del",
            w07.start_valid_time,
            "iniziato",
        )
        w07.status = "1"
        w07.username = request.user.username
        w07.last_update = inizio
        w07.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("a4_a21", w07.id_w07)
        return Response({"id_w07": w07.id_w07})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)

        new = models.W07(
            start_valid_time=today,
            validity=24,
            next_blt_time=tomorrow,
            status="0",  # il nuovo bollettino lo metto in bozza
            last_update=now,
            username=request.user,
        )
        new.save()

        venue = models.Venue.objects.all()
        venue_dict = {}
        for m in venue:
            venue_dict[m.id_venue] = m

        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for mm in time_layouts:
            time_layouts_dict[mm.id_time_layouts] = mm

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for mmm in sky_conditions:
            sky_conditions_dict[mmm.id_sky_condition] = mmm

        venuesA21 = [19, 25, 41, 47, 24, 49, 66, 106, 107, 108]
        time_layouts_a21 = [45, 46, 60, 61, 62, 63, 81, 82]

        metapqueryset = w33models.W33.objects.filter(data_emissione=today).filter(
            status="1"
        )

        with open("config/skycond_firstguess.json") as json_file:
            firstguessdict = json.load(json_file)
            skycond_to_pluv = firstguessdict["skycond_to_pluv"]

        # caso in cui la first guess è letts dal metaprodotto
        if metapqueryset.exists():
            metap = metapqueryset.get()
            id_w33 = metap.id_w33

            datametap = w33models.W33Data.objects.filter(id_w33=id_w33)
            for venueA in venuesA21:
                venuemetapdata = datametap.filter(id_venue=venueA)
                for data in venuemetapdata:
                    try:
                        frzlvl = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data.id_venue
                            )
                            .filter(id_time_layouts=data.id_time_layouts)
                            .filter(id_parametro="FRZLVL")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        frzlvl = None

                    try:
                        termamin = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data.id_venue
                            )
                            .filter(id_time_layouts=data.id_time_layouts)
                            .filter(id_parametro="TERMA_MIN")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        termamin = None

                    temperature_below_zero = False
                    if termamin is not None:
                        if termamin < 0:
                            temperature_below_zero = True

                    try:
                        wind = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data.id_venue
                            )
                            .filter(id_time_layouts=data.id_time_layouts)
                            .filter(id_parametro="WIND_CLASS")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        wind = None

                    notemp = [46, 61, 63]
                    if data.id_time_layouts.id_time_layouts in notemp:
                        temparia = None
                    else:
                        try:
                            temparia = (
                                websitecoremodels.WeatherValues.objects.filter(
                                    id_venue=data.id_venue
                                )
                                .filter(id_time_layouts=data.id_time_layouts)
                                .filter(id_parametro="TERMA")
                                .get()
                                .original_numeric_values
                            )
                        except websitecoremodels.WeatherValues.DoesNotExist:
                            temparia = None

                    new_data = models.W07Data(  # type: ignore
                        id_w07=new,
                        id_venue=data.id_venue,
                        id_time_layouts=data.id_time_layouts,
                        sky_condition=data.id_sky_condition,
                        precipitation_class=skycond_to_pluv[
                            str(data.id_sky_condition.id_sky_condition)
                        ]["precipitation_class"],
                        cumulated_snow=data.cumulated_snow,
                        freezing_level=frzlvl,
                        snow_level=data.snow_level,
                        temperature_below_zero=temperature_below_zero,
                        air_temperature=temparia,
                        wind_class=wind,
                    )
                    new_data.save()
        # Caso in cui la first guess è letta totalmente da weather_values
        else:
            for tl in time_layouts_a21:
                for venueB in venuesA21:
                    try:
                        skycondition = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=venueB
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="SKY_CONDIT")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        skycondition = None

                    try:
                        cumnivo = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=venueB
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="CUM_NIVO")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        cumnivo = None

                    try:
                        snowlev = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=venueB
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="SNOW_LEV")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        snowlev = None

                    try:
                        frzlvl = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=venueB
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="FRZLVL")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        frzlvl = None

                    try:
                        termamin = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=venueB
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="TERMA_MIN")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        termamin = None

                    temperature_below_zero = False
                    if termamin is not None:
                        if termamin < 0:
                            temperature_below_zero = True

                    try:
                        wind = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=venueB
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="WIND_CLASS")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        wind = None

                    notemp = [46, 61, 63]
                    if tl in notemp:
                        temparia = None
                    else:
                        try:
                            temparia = (
                                websitecoremodels.WeatherValues.objects.filter(
                                    id_venue=venueB
                                )
                                .filter(id_time_layouts=tl)
                                .filter(id_parametro="TERMA")
                                .get()
                                .original_numeric_values
                            )
                        except websitecoremodels.WeatherValues.DoesNotExist:
                            temparia = None

                    if cumnivo == 0:
                        cumnivo = None
                    # gestione dei tipi di tempo non previsti dalle autostrade (es. velature)
                    if skycondition == 32:
                        skycondition = Decimal(22)
                    if skycondition in (45, 46):
                        skycondition = Decimal(29)
                    if skycondition is not None:
                        new_data = models.W07Data(  # type: ignore
                            id_w07=new,
                            id_venue=venue_dict[venueB],
                            id_time_layouts=time_layouts_dict[tl],
                            sky_condition=sky_conditions_dict[int(skycondition)],
                            precipitation_class=skycond_to_pluv[str(int(skycondition))][
                                "precipitation_class"
                            ],
                            cumulated_snow=cumnivo,
                            freezing_level=frzlvl,
                            snow_level=snowlev,
                            temperature_below_zero=temperature_below_zero,
                            air_temperature=temparia,
                            wind_class=wind,
                        )
                        new_data.save()

        print("created: ", new)
        return Response({"id_w07": new.id_w07})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W07.objects.get(pk=pk)
        print("w07 reopen:", old)
        old.status = "2"
        old_id_w07 = old.id_w07
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w07_parent = old_id_w07
        new.save()
        # print('created: ', new)
        old_data = models.W07Data.objects.filter(id_w07=old_id_w07)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w07 = new
            new_data.save()

        return Response({"id_w07": new.id_w07})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w07/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for m in sky_conditions:
            sky_conditions_dict[m.id_sky_condition] = m

        id_w07 = next(s["id"] for s in snapshots if s["id_key"] == "id_w07")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w07",
            "id": id_w07,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w07 = models.W07.objects.get(pk=id_w07)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w07":
                print(
                    "id_w07:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w07, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                if snapshot["value_key"] == "sky_condition":
                    print(
                        "id_w07_data:",
                        snapshot["id"],
                        snapshot["value_key"],
                        snapshot["new_value"],
                    )
                    data = models.W07Data.objects.get(pk=snapshot["id"])
                    setattr(
                        data,
                        snapshot["value_key"],
                        sky_conditions_dict[int(snapshot["new_value"])],
                    )
                    data.save()
                    updated += 1
                else:
                    print(
                        "id_w07_data:",
                        snapshot["id"],
                        snapshot["value_key"],
                        snapshot["new_value"],
                    )
                    data = models.W07Data.objects.get(pk=snapshot["id"])
                    setattr(data, snapshot["value_key"], snapshot["new_value"])
                    data.save()
                    updated += 1
        w07.save()
        fine = datetime.datetime.now()
        serializer = W07SerializerFull(w07, context={"request": request})
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


class W07DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows w07 bulletin Data to be viewed or edited
    """

    queryset = models.W07Data.objects.all()
    serializer_class = W07DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W07Data.objects
        w07Data = get_object_or_404(queryset, pk=pk)
        serializer = W07DataSerializer(w07Data, context={"request": request})
        return Response(serializer.data)


class W07a4SVGView(TemplateView):
    template_name = "w07a4.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W07.objects
        w07 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W07SerializerFull(w07)
        autostrada = serializer.data

        autostrada["start_valid_time"] = datetime.datetime.strptime(
            autostrada["start_valid_time"], "%Y-%m-%dT%H:%M:%S"
        )
        autostrada["next_blt_time"] = datetime.datetime.strptime(
            autostrada["next_blt_time"], "%Y-%m-%dT%H:%M:%S"
        )
        autostrada["last_update"] = datetime.datetime.strptime(
            autostrada["last_update"], "%Y-%m-%dT%H:%M:%S"
        )

        days = []
        dayDate = autostrada["start_valid_time"]
        for r in range(3):
            day = dayDate.strftime("%d/%m/%Y")
            days.append(day)
            dayDate = dayDate + datetime.timedelta(days=1)

        venue = models.Venue.objects.all()
        venue_dict = {}
        for m in venue:
            venue_dict[str(m.id_venue)] = m.description

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for mmm in sky_conditions:
            sky_conditions_dict[mmm.id_sky_condition] = mmm.description_ita

        precipitation_classes = {
            "0": "Assente",
            "1": "Debole",
            "2": "Moderata",
            "3": "Forte",
            "4": "Molto forte",
        }

        wind_classes = {
            "0": "Calmo",
            "1": "Debole",
            "2": "Moderato",
            "3": "Forte",
            "4": "Molto forte",
        }

        tmp: dict = {}
        for data in autostrada["w07data_set"]:
            if not data["id_venue"] in tmp:
                tmp[data["id_venue"]] = {}
            if not data["id_time_layouts"] in tmp[data["id_venue"]]:
                tmp[data["id_venue"]][data["id_time_layouts"]] = {}
            tmp[data["id_venue"]][data["id_time_layouts"]] = data
            tmp[data["id_venue"]][data["id_time_layouts"]]["precipitation_class"] = (
                precipitation_classes[
                    str(
                        tmp[data["id_venue"]][data["id_time_layouts"]][
                            "precipitation_class"
                        ]
                    )
                ]
            )
            tmp[data["id_venue"]][data["id_time_layouts"]]["wind_class"] = wind_classes[
                str(tmp[data["id_venue"]][data["id_time_layouts"]]["wind_class"])
            ]
            if tmp[data["id_venue"]][data["id_time_layouts"]]["cumulated_snow"] is None:
                tmp[data["id_venue"]][data["id_time_layouts"]]["cumulated_snow"] = "NO"
            if (
                tmp[data["id_venue"]][data["id_time_layouts"]]["temperature_below_zero"]
                is False
            ):
                tmp[data["id_venue"]][data["id_time_layouts"]][
                    "temperature_below_zero"
                ] = "NO"
            else:
                tmp[data["id_venue"]][data["id_time_layouts"]][
                    "temperature_below_zero"
                ] = "SI"

            tmp[data["id_venue"]][data["id_time_layouts"]]["sky_desc"] = (
                sky_conditions_dict[
                    tmp[data["id_venue"]][data["id_time_layouts"]]["sky_condition"]
                ]
            )
            if (
                tmp[data["id_venue"]][data["id_time_layouts"]]["air_temperature"]
                is not None
            ):
                tmp[data["id_venue"]][data["id_time_layouts"]]["air_temperature"] = tmp[
                    data["id_venue"]
                ][data["id_time_layouts"]]["air_temperature"]
            else:
                tmp[data["id_venue"]][data["id_time_layouts"]]["air_temperature"] = ""

        autostrada["w07data_set"] = tmp
        context = {
            "w07": autostrada,
            "venues": venue_dict,
            "days": days,
            "title": "Autostrada A4",
        }
        return context


class W07a21SVGView(TemplateView):
    template_name = "w07a21.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W07.objects
        w07 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W07SerializerFull(w07)
        autostrada = serializer.data

        autostrada["start_valid_time"] = datetime.datetime.strptime(
            autostrada["start_valid_time"], "%Y-%m-%dT%H:%M:%S"
        )
        autostrada["next_blt_time"] = datetime.datetime.strptime(
            autostrada["next_blt_time"], "%Y-%m-%dT%H:%M:%S"
        )
        autostrada["last_update"] = datetime.datetime.strptime(
            autostrada["last_update"], "%Y-%m-%dT%H:%M:%S"
        )

        days = []
        dayDate = autostrada["start_valid_time"]
        for r in range(3):
            day = dayDate.strftime("%d/%m/%Y")
            days.append(day)
            dayDate = dayDate + datetime.timedelta(days=1)

        venue = models.Venue.objects.all()
        venue_dict = {}
        for m in venue:
            venue_dict[str(m.id_venue)] = m.description

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for mmm in sky_conditions:
            sky_conditions_dict[mmm.id_sky_condition] = mmm.description_ita

        precipitation_classes = {
            "0": "Assente",
            "1": "Debole",
            "2": "Moderata",
            "3": "Forte",
            "4": "Molto forte",
        }

        wind_classes = {
            "0": "Calmo",
            "1": "Debole",
            "2": "Moderato",
            "3": "Forte",
            "4": "Molto forte",
        }

        tmp: dict = {}
        for data in autostrada["w07data_set"]:
            if not data["id_venue"] in tmp:
                tmp[data["id_venue"]] = {}
            if not data["id_time_layouts"] in tmp[data["id_venue"]]:
                tmp[data["id_venue"]][data["id_time_layouts"]] = {}
            tmp[data["id_venue"]][data["id_time_layouts"]] = data
            tmp[data["id_venue"]][data["id_time_layouts"]]["precipitation_class"] = (
                precipitation_classes[
                    str(
                        tmp[data["id_venue"]][data["id_time_layouts"]][
                            "precipitation_class"
                        ]
                    )
                ]
            )
            tmp[data["id_venue"]][data["id_time_layouts"]]["wind_class"] = wind_classes[
                str(tmp[data["id_venue"]][data["id_time_layouts"]]["wind_class"])
            ]
            if tmp[data["id_venue"]][data["id_time_layouts"]]["cumulated_snow"] is None:
                tmp[data["id_venue"]][data["id_time_layouts"]]["cumulated_snow"] = "NO"
            if (
                tmp[data["id_venue"]][data["id_time_layouts"]]["temperature_below_zero"]
                is False
            ):
                tmp[data["id_venue"]][data["id_time_layouts"]][
                    "temperature_below_zero"
                ] = "NO"
            else:
                tmp[data["id_venue"]][data["id_time_layouts"]][
                    "temperature_below_zero"
                ] = "SI"

            tmp[data["id_venue"]][data["id_time_layouts"]]["sky_desc"] = (
                sky_conditions_dict[
                    tmp[data["id_venue"]][data["id_time_layouts"]]["sky_condition"]
                ]
            )
            if (
                tmp[data["id_venue"]][data["id_time_layouts"]]["air_temperature"]
                is not None
            ):
                tmp[data["id_venue"]][data["id_time_layouts"]]["air_temperature"] = tmp[
                    data["id_venue"]
                ][data["id_time_layouts"]]["air_temperature"]
            else:
                tmp[data["id_venue"]][data["id_time_layouts"]]["air_temperature"] = ""

        autostrada["w07data_set"] = tmp
        context = {
            "w07": autostrada,
            "venues": venue_dict,
            "days": days,
            "title": "Autostrada A21",
        }
        return context


class W07a4PDFView(W07a4SVGView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template="w07a4.svg",
            context=self.get_context_data(**kwargs),
            filename="w07_a4.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class W07a21PDFView(W07a21SVGView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template="w07a21.svg",
            context=self.get_context_data(**kwargs),
            filename="w07_a21.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response
