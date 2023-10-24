#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json

# import os
# import tempfile
# from contextlib import closing
# from subprocess import call
# import requests
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

from w12.back import models
from w12.back.serializers import W12DataSerializer, W12Serializer, W12SerializerFull
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


class W12View(viewsets.ModelViewSet):
    """
    API endpoint that allows W12 bulletins to be viewed or edited
    """

    queryset = models.W12.objects.order_by("-last_update", "-pk")
    serializer_class = W12Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        month = self.request.query_params.get("month", "all")
        year = self.request.query_params.get("year", "all")
        if month != "all":
            queryset = (
                self.get_queryset()
                .filter(start_valid_time__year=year)
                .filter(start_valid_time__month=month)
            )
        elif year != "all":
            queryset = self.filter_queryset(
                self.get_queryset().filter(start_valid_time__year=year)
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
        queryset = models.W12.objects
        w12 = get_object_or_404(queryset, pk=pk)
        serializer = W12SerializerFull(w12, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W12.objects
        if (
            instance.id_w12_parent
            and queryset.filter(pk=instance.id_w12_parent).exists()
        ):
            w12 = get_object_or_404(queryset, pk=instance.id_w12_parent)
            w12.status = "1"
            if not User.objects.filter(username=w12.username).exists():
                print("perform_destroy non trovo l'utente " + w12.username)
                w12.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w12.save()
        instance.delete()

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w12 = models.W12.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w12.id_w12,
            "del",
            w12.start_valid_time,
            "iniziato",
        )
        w12.status = "1"
        w12.username = request.user.username
        w12.last_update = inizio
        w12.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("a7_a26", w12.id_w12)
        return Response({"id_w12": w12.id_w12})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)

        new = models.W12(
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

        venuesA26 = [99, 100, 101, 102, 103, 104, 105]
        time_layouts_a26 = [45, 46, 60, 61, 62, 63, 81, 82]

        metapqueryset = w33models.W33.objects.filter(data_emissione=today).filter(
            status="1"
        )

        with open("config/skycond_firstguess.json") as json_file:
            firstguessdict = json.load(json_file)
            skycond_to_coptot = firstguessdict["skycond_to_coptot"]
            skycond_to_pluv = firstguessdict["skycond_to_pluv_A26"]

        if metapqueryset.exists():
            metap = metapqueryset.get()
            id_w33 = metap.id_w33

            datametap = w33models.W33Data.objects.filter(id_w33=id_w33)
            for venueA in venuesA26:
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
                            .filter(id_parametro="WIND_BEAUF")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        wind = None

                    new_data = models.W12Data(  # type: ignore
                        id_w12=new,
                        id_venue=data.id_venue,
                        id_time_layouts=data.id_time_layouts,
                        sky_condition=data.id_sky_condition,
                        cloud_amount=skycond_to_coptot[
                            str(data.id_sky_condition.id_sky_condition)
                        ]["cop_tot"],
                        precipitation_class=skycond_to_pluv[
                            str(data.id_sky_condition.id_sky_condition)
                        ]["precipitation_class"],
                        cumulated_snow=data.cumulated_snow,
                        freezing_level=frzlvl,
                        snow_level=data.snow_level,
                        temperature_below_zero=temperature_below_zero,
                        risk_freezing_rain=False,
                        vis_inf_1000=False,
                        vis_inf_1000_reason=None,
                        wind_class=wind,
                    )
                    new_data.save()
        else:
            for tl in time_layouts_a26:
                for venueB in venuesA26:
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
                            .filter(id_parametro="WIND_BEAUF")
                            .get()
                            .original_numeric_values
                        )
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        wind = None

                    if cumnivo == 0:
                        cumnivo = None

                    if skycondition is not None:
                        new_data = models.W12Data(  # type: ignore
                            id_w12=new,
                            id_venue=venue_dict[venueB],
                            id_time_layouts=time_layouts_dict[tl],
                            sky_condition=sky_conditions_dict[int(skycondition)],
                            cloud_amount=skycond_to_coptot[str(int(skycondition))][
                                "cop_tot"
                            ],
                            precipitation_class=skycond_to_pluv[str(int(skycondition))][
                                "precipitation_class"
                            ],
                            cumulated_snow=cumnivo,
                            freezing_level=frzlvl,
                            snow_level=snowlev,
                            temperature_below_zero=temperature_below_zero,
                            risk_freezing_rain=False,
                            vis_inf_1000=False,
                            vis_inf_1000_reason=None,
                            wind_class=wind,
                        )
                        new_data.save()

        print("created: ", new)
        return Response({"id_w12": new.id_w12})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W12.objects.get(pk=pk)
        print("w12 reopen:", old)
        old.status = "2"
        old_id_w12 = old.id_w12
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w12_parent = old_id_w12
        new.save()
        # print('created: ', new)
        old_data = models.W12Data.objects.filter(id_w12=old_id_w12)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w12 = new
            new_data.save()

        return Response({"id_w12": new.id_w12})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w12/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for m in sky_conditions:
            sky_conditions_dict[m.id_sky_condition] = m

        id_w12 = next(s["id"] for s in snapshots if s["id_key"] == "id_w12")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w12",
            "id": id_w12,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w12 = models.W12.objects.get(pk=id_w12)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w12":
                print(
                    "id_w12:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w12, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                if snapshot["value_key"] == "sky_condition":
                    print(
                        "id_w12_data:",
                        snapshot["id"],
                        snapshot["value_key"],
                        snapshot["new_value"],
                    )
                    data = models.W12Data.objects.get(pk=snapshot["id"])
                    setattr(
                        data,
                        snapshot["value_key"],
                        sky_conditions_dict[int(snapshot["new_value"])],
                    )
                    data.save()
                    updated += 1
                else:
                    print(
                        "id_w12_data:",
                        snapshot["id"],
                        snapshot["value_key"],
                        snapshot["new_value"],
                    )
                    data = models.W12Data.objects.get(pk=snapshot["id"])
                    setattr(data, snapshot["value_key"], snapshot["new_value"])
                    data.save()
                    updated += 1
        w12.save()
        fine = datetime.datetime.now()
        serializer = W12SerializerFull(w12, context={"request": request})
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


class W12DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W12 bulletin Data to be viewed or edited
    """

    queryset = models.W12Data.objects.all()
    serializer_class = W12DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W12Data.objects
        w12Data = get_object_or_404(queryset, pk=pk)
        serializer = W12DataSerializer(w12Data, context={"request": request})
        return Response(serializer.data)


class W12SVGView(TemplateView):
    template_name = "a26.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W12.objects
        w12 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W12SerializerFull(w12)
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
            "1": "Molto debole",
            "2": "Debole",
            "3": "Moderata",
            "4": "Forte",
            "5": "Molto forte",
        }

        tmp: dict = {}
        for data in autostrada["w12data_set"]:
            if not data["id_venue"] in tmp:
                tmp[data["id_venue"]] = {}
            if not data["id_time_layouts"] in tmp[data["id_venue"]]:
                tmp[data["id_venue"]][data["id_time_layouts"]] = {}
            tmp[data["id_venue"]][data["id_time_layouts"]] = data
            tmp[data["id_venue"]][data["id_time_layouts"]][
                "precipitation_class"
            ] = precipitation_classes[
                str(
                    tmp[data["id_venue"]][data["id_time_layouts"]][
                        "precipitation_class"
                    ]
                )
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
            tmp[data["id_venue"]][data["id_time_layouts"]][
                "sky_desc"
            ] = sky_conditions_dict[
                tmp[data["id_venue"]][data["id_time_layouts"]]["sky_condition"]
            ]

        autostrada["w12data_set"] = tmp
        context = {
            "w12": autostrada,
            "venues": venue_dict,
            "days": days,
            "title": "Autostrada A7-A26",
        }
        return context


class W12PDFView(W12SVGView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="w12.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response
