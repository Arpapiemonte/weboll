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
from wkhtmltopdf.views import PDFTemplateResponse

from w33.back import models
from w33.back.serializers import W33DataSerializer, W33Serializer, W33SerializerFull

# from website.common.tasks import send_with_celery
from website.common.views import (  # ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core import models as websitecoremodels

# from rest_framework_xml.renderers import XMLRenderer
# from wkhtmltopdf.views import PDFTemplateResponse


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W33View(viewsets.ModelViewSet):
    """
    API endpoint that allows W33 bulletins to be viewed or edited
    """

    queryset = models.W33.objects.order_by("-last_update", "-pk")
    serializer_class = W33Serializer
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

    def retrieve(self, request, pk=None):
        queryset = models.W33.objects
        w33 = get_object_or_404(queryset, pk=pk)
        serializer = W33SerializerFull(w33, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W33.objects
        if (
            instance.id_w33_parent
            and queryset.filter(pk=instance.id_w33_parent).exists()
        ):
            w33 = get_object_or_404(queryset, pk=instance.id_w33_parent)
            w33.status = "1"
            if not User.objects.filter(username=w33.username).exists():
                print("perform_destroy non trovo l'utente " + w33.username)
                w33.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w33.save()
        instance.delete()

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w33 = models.W33.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w33.id_w33,
            "del",
            w33.data_emissione,
            "iniziato",
        )
        w33.status = "1"
        w33.username = request.user.username
        w33.last_update = inizio
        w33.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        # send_with_celery("bis", w33.id_w33)
        return Response({"id_w33": w33.id_w33})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)

        old_queryset = models.W33.objects.filter(status="1").order_by("-last_update")

        if old_queryset.exists():
            old = old_queryset.latest("pk")
        else:
            old = None

        if old is not None:
            # gestione anno nuovo
            if old.data_emissione.year < today.year:
                print("new(): cambio dell'anno imposto il sequenziale a 1")
                new_seq = 1
            else:
                last_seq_num = (
                    models.W33.objects.filter(data_emissione__year=today.year)
                    .exclude(status="0")
                    .latest("seq_num")
                    .seq_num
                )
                new_seq = last_seq_num + 1
        else:
            print("primo bollettino")
            new_seq = 1

        new = models.W33(
            data_emissione=today,
            seq_num=new_seq,  # incremento il sequenziale
            status="0",  # il nuovo bollettino lo metto in bozza
            last_update=now,
            username=request.user,
        )
        new.save()
        print("created: ", new)

        venue = models.Venue.objects.all()
        venue_dict = {}
        for m in venue:
            venue_dict[str(m.id_venue)] = m

        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for mm in time_layouts:
            time_layouts_dict[mm.id_time_layouts] = mm

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for mmm in sky_conditions:
            sky_conditions_dict[mmm.id_sky_condition] = mmm

        with open("config/w33_data.json") as json_file:
            w33_data_config = json.load(json_file)

        old_w33_data_queryset = models.W33.objects.filter(
            data_emissione=yesterday.date()
        ).filter(status="1")
        snow_icons = [9, 21, 7, 26, 18, 44]

        if old_w33_data_queryset.exists():
            yesterday_metap = old_w33_data_queryset.get()
            yesterday_id = yesterday_metap.id_w33

            w33_data_d1_h3 = models.W33Data.objects.filter(id_w33=yesterday_id).filter(
                id_time_layouts=62
            )
            for data in w33_data_d1_h3:
                new_data = models.W33Data(
                    id_w33=new,
                    id_venue=data.id_venue,
                    id_time_layouts=time_layouts_dict[45],
                    id_sky_condition=data.id_sky_condition,
                    cumulated_snow=data.cumulated_snow,
                    snow_level=data.snow_level,
                )
                new_data.save()
            w33_data_d1_h4 = models.W33Data.objects.filter(id_w33=yesterday_id).filter(
                id_time_layouts=63
            )
            for data in w33_data_d1_h4:
                new_data = models.W33Data(
                    id_w33=new,
                    id_venue=data.id_venue,
                    id_time_layouts=time_layouts_dict[46],
                    id_sky_condition=data.id_sky_condition,
                    cumulated_snow=data.cumulated_snow,
                    snow_level=data.snow_level,
                )
                new_data.save()
            time_layouts_autostrade_d0 = [
                60,
                61,
                62,
                63,
                81,
                82,
            ]

            for data1 in w33_data_config:
                for tl in time_layouts_autostrade_d0:
                    try:
                        w_value_sky_condit = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data1["id_venue"]
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="SKY_CONDIT")
                            .get()
                        ).original_numeric_values
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        w_value_sky_condit = None

                    try:
                        w_value_nivo = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data1["id_venue"]
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="CUM_NIVO")
                            .get()
                        ).original_numeric_values
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        w_value_nivo = None

                    try:
                        w_value_snow_lev = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data1["id_venue"]
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="SNOW_LEV")
                            .get()
                        ).original_numeric_values
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        w_value_snow_lev = None

                    nivo_value = w_value_nivo
                    if w_value_sky_condit not in snow_icons and w_value_nivo == 0:
                        nivo_value = None
                    # poiché le velature non sono accettate nel set di icone delle autostrade,
                    # sono convertite in "poco nuvoloso", stessa cosa per vento e sole e vento e nuvola
                    if w_value_sky_condit == 32:
                        w_value_sky_condit = Decimal(22)
                    if w_value_sky_condit in (45, 46):
                        w_value_sky_condit = Decimal(29)
                    if w_value_sky_condit is not None:
                        new_data = models.W33Data(  # type: ignore
                            id_w33=new,
                            id_venue=venue_dict[data1["id_venue"]],
                            id_time_layouts=time_layouts_dict[tl],
                            id_sky_condition=sky_conditions_dict[
                                int(w_value_sky_condit)
                            ],
                            cumulated_snow=nivo_value,
                            snow_level=w_value_snow_lev,
                        )
                        new_data.save()
        else:
            time_layouts_autostrade_d1 = [
                45,
                46,
                60,
                61,
                62,
                63,
                81,
                82,
            ]

            for data2 in w33_data_config:
                for tl in time_layouts_autostrade_d1:
                    try:
                        w_value_sky_condit = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data2["id_venue"]
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="SKY_CONDIT")
                            .get()
                        ).original_numeric_values
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        w_value_sky_condit = None

                    try:
                        w_value_nivo = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data2["id_venue"]
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="CUM_NIVO")
                            .get()
                        ).original_numeric_values
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        w_value_nivo = None

                    try:
                        w_value_snow_lev = (
                            websitecoremodels.WeatherValues.objects.filter(
                                id_venue=data2["id_venue"]
                            )
                            .filter(id_time_layouts=tl)
                            .filter(id_parametro="SNOW_LEV")
                            .get()
                        ).original_numeric_values
                    except websitecoremodels.WeatherValues.DoesNotExist:
                        w_value_snow_lev = None

                    nivo_value = w_value_nivo
                    if w_value_sky_condit not in snow_icons and w_value_nivo == 0:
                        nivo_value = None
                    # poiché le velature non sono accettate nel set di icone delle autostrade,
                    # sono convertite in "poco nuvoloso"
                    if w_value_sky_condit == 32:
                        w_value_sky_condit = Decimal(22)
                    if w_value_sky_condit in (45, 46):
                        w_value_sky_condit = Decimal(29)
                    if w_value_sky_condit is not None:
                        new_data = models.W33Data(  # type: ignore
                            id_w33=new,
                            id_venue=venue_dict[data2["id_venue"]],
                            id_time_layouts=time_layouts_dict[tl],
                            id_sky_condition=sky_conditions_dict[
                                int(w_value_sky_condit)
                            ],
                            cumulated_snow=nivo_value,
                            snow_level=w_value_snow_lev,
                        )
                        new_data.save()

        return Response({"id_w33": new.id_w33})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W33.objects.get(pk=pk)
        print("w33 reopen:", old)
        old.status = "2"
        old_id_w33 = old.id_w33
        old.save()
        new_seq = old.seq_num
        if new_seq is not None:
            new_seq = new_seq + 1
        else:
            new_seq = 1
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.seq_num = new_seq
        new.last_update = now
        new.username = request.user
        new.id_w33_parent = old_id_w33
        new.save()
        # print('created: ', new)
        old_data = models.W33Data.objects.filter(id_w33=old_id_w33)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w33 = new
            new_data.save()

        return Response({"id_w33": new.id_w33})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w33/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data

        sky_conditions = models.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for m in sky_conditions:
            sky_conditions_dict[m.id_sky_condition] = m

        print(snapshots)
        id_w33 = next(s["id"] for s in snapshots if s["id_key"] == "id_w33")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w33",
            "id": id_w33,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w33 = models.W33.objects.get(pk=id_w33)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w33":
                print(
                    "id_w33:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w33, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                if snapshot["value_key"] == "id_sky_condition":
                    print(
                        "id_w33_data:",
                        snapshot["id"],
                        snapshot["value_key"],
                        snapshot["new_value"],
                    )
                    data = models.W33Data.objects.get(pk=snapshot["id"])
                    setattr(
                        data,
                        snapshot["value_key"],
                        sky_conditions_dict[int(snapshot["new_value"])],
                    )
                    data.save()
                    updated += 1
                else:
                    print(
                        "id_w33_data:",
                        snapshot["id"],
                        snapshot["value_key"],
                        snapshot["new_value"],
                    )
                    data = models.W33Data.objects.get(pk=snapshot["id"])
                    setattr(data, snapshot["value_key"], snapshot["new_value"])
                    data.save()
                    updated += 1
        w33.save()
        fine = datetime.datetime.now()
        serializer = W33SerializerFull(w33, context={"request": request})
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


class W33DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W33 bulletin Data to be viewed or edited
    """

    queryset = models.W33Data.objects.all()
    serializer_class = W33DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W33Data.objects
        w33Data = get_object_or_404(queryset, pk=pk)
        serializer = W33DataSerializer(w33Data, context={"request": request})
        return Response(serializer.data)


class HtmlView(TemplateView):
    template_name = "mpa.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W33.objects
        print("kwargs", kwargs)
        w33 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W33SerializerFull(w33)
        mpa = serializer.data
        context = {
            "mpa": mpa,
        }
        return context


class PdfView(HtmlView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
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
