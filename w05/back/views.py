#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import copy
import datetime
import json
import os
import tempfile
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
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w05.back.serializers import (
    ClassesSerializer,
    SkyConditionSerializer,
    VenueSerializer,
    W05ClassesSerializer,
    W05DataSerializer,
    W05Serializer,
    W05SerializerFull,
)
from website.common.tasks import send_with_celery
from website.common.views import (
    BulletinDraftLocked,
    ExistingTodayBulletin,
    StandardResultsSetPagination,
)
from website.core import models


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W05View(viewsets.ModelViewSet):
    """
    API endpoint that allows W05 bulletins to be viewed or edited
    """

    queryset = models.W05.objects.order_by("-last_update", "-seq_num", "-pk")
    serializer_class = W05Serializer
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

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W05.objects
        if (
            instance.id_w05_parent
            and queryset.filter(pk=instance.id_w05_parent).exists()
        ):
            w05 = get_object_or_404(queryset, pk=instance.id_w05_parent)
            w05.status = "1"
            if not User.objects.filter(username=w05.username).exists():
                print("perform_destroy non trovo l'utente " + w05.username)
                w05.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w05.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W05.objects
        w05 = get_object_or_404(queryset, pk=pk)
        serializer = W05SerializerFull(w05, context={"request": request})
        return Response(serializer.data)

    # Action for Json Output
    @action(detail=True, methods=["get"], renderer_classes=[JSONRenderer])
    def json(self, request, pk):
        queryset = models.W05.objects.filter(pk=pk)
        w05 = get_object_or_404(queryset, pk=pk)
        serializer = W05SerializerFull(w05, context={"request": request})
        return Response(serializer.data)

    # Action for XML output
    @action(detail=True, methods=["get"], renderer_classes=[XMLRenderer])
    def xml(self, request, pk):
        queryset = models.W05.objects.filter(pk=pk)
        w05 = get_object_or_404(queryset, pk=pk)
        serializer = W05SerializerFull(w05, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # crea il nuovo bollettino di oggi traslando le date dall'ultimo di ieri a status 1 solo per i parametri
        # 'COP_TOT', 'FRZLVL', 'PLUV', 'VELV', 'WFOP'
        # il resto lo prende da weather_values
        delimiter = "__"

        def HashW05Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
            return (
                str(id_venue)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(id_time_layouts)
            )

        def HashW05Classes(
            id_venue, id_parametro, id_aggregazione, id_time_layouts, id_classes
        ):
            return (
                str(id_venue)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(id_time_layouts)
                + delimiter
                + str(id_classes)
            )

        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today.replace(hour=14, minute=0, second=0, microsecond=0)
        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = emissione + datetime.timedelta(days=1)

        today_bulletins = models.W05.objects.filter(
            start_valid_time__date=today.date()
        ).count()
        if today_bulletins >= 1:
            raise ExistingTodayBulletin()

        create_empty = False
        if (
            not models.W05.objects.filter(start_valid_time__date=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w05 = (
                models.W05.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w05 = (
                models.W05.objects.filter(start_valid_time__date=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w05.id_w05,
            "del",
            old_w05.start_valid_time,
            "iniziato",
        )
        # aumento il sequenziale perchè è una nuova emissione
        new_seq = old_w05.seq_num
        if new_seq is not None:
            new_seq = new_seq + 1
        else:
            print("new(): attenzione sequenziale a None imposto il sequenziale a 1")
            new_seq = 1
        # gestione anno nuovo
        if old_w05.start_valid_time.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            new_seq = 1

        if create_empty:
            situation = ""
        else:
            situation = str(old_w05.situation)

        new = models.W05(
            start_valid_time=emissione,  # devono essere le 14
            validity=84,
            next_blt_time=tomorrow,  # controlla orario
            situation=situation,
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            seq_num=new_seq,
            version=1,
        )
        new.save()
        fine = datetime.datetime.now()
        print(
            "leggo venues ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        venues = models.Venue.objects.all()
        venues_dict = {}
        for v in venues:
            venues_dict[str(v.id_venue)] = v
        fine = datetime.datetime.now()
        print(
            "leggo parametro ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        parametri = models.Parametro.objects.all().select_related("id_unita_misura")
        parametri_dict = {}
        for p in parametri:
            parametri_dict[p.id_parametro] = p
        fine = datetime.datetime.now()
        print(
            "leggo aggregazione ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        aggregazione = models.Aggregazione.objects.all().select_related(
            "id_unita_misura"
        )
        aggregazione_dict = {}
        for a in aggregazione:
            aggregazione_dict[str(a.id_aggregazione)] = a
        fine = datetime.datetime.now()
        print(
            "leggo time_layouts ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for t in time_layouts:
            time_layouts_dict[str(t.id_time_layouts)] = t
        fine = datetime.datetime.now()
        print(
            "leggo classes ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        classes = models.Classes.objects.all().select_related("id_parametro")
        classes_dict = {}
        for c in classes:
            classes_dict[str(c.id_classes)] = c
        fine = datetime.datetime.now()
        print(
            "leggo classes_value ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        classes_value = models.ClassesValue.objects.all().select_related("id_classes")
        classes_value_dict = {}
        for c in classes_value:  # type: ignore
            classes_value_dict[str(c.id_classes_value)] = c  # type: ignore

        if not create_empty:
            fine = datetime.datetime.now()
            print(
                "leggo w05_data ",
                abs((fine - inizio).total_seconds()),
                "secondi",
            )

            w05_data_old = models.W05Data.objects.filter(
                id_w05=old_w05.id_w05
            ).select_related(
                "id_venue",
                "id_parametro",
                "id_trend",
                "id_aggregazione",
                "id_time_layouts",
            )
            w05_data_old_dict = {}
            for w in w05_data_old:
                w05_data_old_dict[
                    HashW05Data(
                        w.id_venue.id_venue,
                        w.id_parametro.id_parametro,
                        w.id_aggregazione.id_aggregazione,
                        w.id_time_layouts.id_time_layouts,
                    )
                ] = w
                fine = datetime.datetime.now()
            print(
                "leggo w05_classes ",
                abs((fine - inizio).total_seconds()),
                "secondi",
            )
            w05_classes_old = models.W05Classes.objects.filter(
                id_w05=old_w05.id_w05
            ).select_related(
                "id_venue",
                "id_parametro",
                "id_aggregazione",
                "id_time_layouts",
                "id_classes",
                "id_classes_value",
            )
            w05_classes_old_dict = {}
            for c in w05_classes_old:  # type: ignore
                w05_classes_old_dict[
                    HashW05Classes(
                        c.id_venue.id_venue,  # type: ignore
                        c.id_parametro.id_parametro,
                        c.id_aggregazione.id_aggregazione,  # type: ignore
                        c.id_time_layouts.id_time_layouts,  # type: ignore
                        c.id_classes.id_classes,  # type: ignore
                    )
                ] = c

        fine = datetime.datetime.now()
        print(
            "leggo weather_values ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        weather_values = models.WeatherValues.objects.all().select_related(
            "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
        )
        weather_values_dict = {}
        for w in weather_values:  # type: ignore
            weather_values_dict[
                HashW05Data(
                    w.id_venue.id_venue,
                    w.id_parametro.id_parametro,
                    w.id_aggregazione.id_aggregazione,
                    w.id_time_layouts.id_time_layouts,
                )
            ] = w

        # carico la configurazione json per sapere quanti record ci devono essere su w05_data
        with open("config/w05_data.json") as json_file:
            w05_data_config = json.load(json_file)
        # sistema il json di configurazione in modo da avere come chiave primaria
        # id_venue__id_parametro__id_aggregazione__id_time_layouts
        w05_data_da_inserire = {}  # type: ignore
        for w in w05_data_config:
            w05_data_da_inserire[
                HashW05Data(
                    w05_data_config[w]["id_venue"],
                    w05_data_config[w]["id_parametro"],
                    w05_data_config[w]["id_aggregazione"],
                    w05_data_config[w]["id_time_layouts"],
                )
            ] = None

        fine = datetime.datetime.now()
        print(
            "creo i w05_data vuoti ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        # creo tutti i w05_data nuovi
        w05_data_new_dict = {}
        for w in w05_data_da_inserire:
            w05_data_tmp = w.split(delimiter)  # type: ignore
            my_time_layouts = time_layouts_dict[w05_data_tmp[3]]
            text_value = None
            if w05_data_tmp[1] == "WFR":
                if w05_data_tmp[3] == "48":
                    text_value = "95"
                elif w05_data_tmp[3] == "66":
                    text_value = "90"
                elif w05_data_tmp[3] == "83":
                    text_value = "80"
                elif w05_data_tmp[3] == "100":
                    text_value = "70"
            if w05_data_tmp[1] == "WFOP":
                if w05_data_tmp[3] == "100":
                    text_value = "nulla da segnalare."
            w05_data_new_dict[
                HashW05Data(
                    w05_data_tmp[0], w05_data_tmp[1], w05_data_tmp[2], w05_data_tmp[3]
                )
            ] = models.W05Data(
                id_w05=new,
                id_venue=venues_dict[w05_data_tmp[0]],
                id_parametro=parametri_dict[w05_data_tmp[1]],
                id_aggregazione=aggregazione_dict[w05_data_tmp[2]],
                numeric_value=None,
                id_trend=None,
                text_value=text_value,
                id_time_layouts=my_time_layouts,
                start_valid_time=today
                + datetime.timedelta(days=my_time_layouts.start_day_offset)
                + datetime.timedelta(hours=my_time_layouts.start_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.start_time.minute),
                end_valid_time=today
                + datetime.timedelta(days=my_time_layouts.end_day_offset)  # type: ignore
                + datetime.timedelta(hours=my_time_layouts.end_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.end_time.minute),
            )

        # carico la configurazione json per sapere quanti record ci devono essere su w05_classes
        with open("config/w05_classes.json") as json_file:
            w05_classes_config = json.load(json_file)
        # sistema il json di configurazione in modo da avere come chiave primaria
        # id_venue__id_parametro__id_aggregazione__id_time_layouts
        w05_classes_da_inserire = {}  # type: ignore
        for w in w05_classes_config:
            w05_classes_da_inserire[
                HashW05Classes(
                    w05_classes_config[w]["id_venue"],
                    w05_classes_config[w]["id_parametro"],
                    w05_classes_config[w]["id_aggregazione"],
                    w05_classes_config[w]["id_time_layouts"],
                    w05_classes_config[w]["id_classes"],
                )
            ] = None
        fine = datetime.datetime.now()
        print(
            "creo i w05_classes vuoti ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        # inserisco tutti i w05_classes
        w05_classes_new_dict = {}
        for w05_classes in w05_classes_da_inserire:
            w05_classes_tmp = w05_classes.split(delimiter)
            my_time_layouts = time_layouts_dict[w05_classes_tmp[3]]
            w05_classes_new_dict[
                HashW05Classes(
                    w05_classes_tmp[0],
                    w05_classes_tmp[1],
                    w05_classes_tmp[2],
                    w05_classes_tmp[3],
                    w05_classes_tmp[4],
                )
            ] = models.W05Classes(
                id_w05=new,
                id_venue=venues_dict[w05_classes_tmp[0]],
                id_parametro=parametri_dict[w05_classes_tmp[1]],
                id_aggregazione=aggregazione_dict[w05_classes_tmp[2]],
                id_classes_value=classes_value_dict[
                    str(classes_dict[w05_classes_tmp[4]].id_classes + 80)
                ],  # il valore nullo
                id_classes=classes_dict[w05_classes_tmp[4]],
                id_time_layouts=my_time_layouts,
                start_valid_time=today
                + datetime.timedelta(days=my_time_layouts.start_day_offset)
                + datetime.timedelta(hours=my_time_layouts.start_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.start_time.minute),
                end_valid_time=today
                + datetime.timedelta(days=my_time_layouts.end_day_offset)  # type: ignore
                + datetime.timedelta(hours=my_time_layouts.end_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.end_time.minute),
            )

        # replico i campi testuali traslando le date per i primi 3 giorni
        if not create_empty:
            fine = datetime.datetime.now()
            print(
                "inizio w05_data di ieri ",
                abs((fine - inizio).total_seconds()),
                "secondi",
            )
            map_time_layouts = {"66": "48", "83": "66", "100": "83"}
            for w_old in w05_data_old_dict:
                w_old_keys = w_old.split(delimiter)
                if w_old_keys[1] in ["COP_TOT", "FRZLVL", "PLUV", "VELV", "WFOP"]:
                    if w_old_keys[3] in map_time_layouts.keys():
                        w_new_keys = w_old.split(delimiter)
                        w_new_keys[3] = map_time_layouts[w_old_keys[3]]
                        # nel caso del FRZLVL del time_layouts 66 quando passa a 48 cambia aggregazione da 912 a 914
                        if (
                            w_old_keys[0] == "67"
                            and w_old_keys[1] == "FRZLVL"
                            and w_old_keys[2] == "912"
                            and w_old_keys[3] == "66"
                            and w_new_keys[3] == "48"
                        ):
                            w_new_keys[2] = "914"
                        if (
                            HashW05Data(
                                w_new_keys[0],
                                w_new_keys[1],
                                w_new_keys[2],
                                w_new_keys[3],
                            )
                            in w05_data_new_dict
                        ):
                            w05_data_new_dict[
                                HashW05Data(
                                    w_new_keys[0],
                                    w_new_keys[1],
                                    w_new_keys[2],
                                    w_new_keys[3],
                                )
                            ].numeric_value = w05_data_old_dict[
                                HashW05Data(
                                    w_old_keys[0],
                                    w_old_keys[1],
                                    w_old_keys[2],
                                    w_old_keys[3],
                                )
                            ].numeric_value
                            w05_data_new_dict[
                                HashW05Data(
                                    w_new_keys[0],
                                    w_new_keys[1],
                                    w_new_keys[2],
                                    w_new_keys[3],
                                )
                            ].id_trend = w05_data_old_dict[
                                HashW05Data(
                                    w_old_keys[0],
                                    w_old_keys[1],
                                    w_old_keys[2],
                                    w_old_keys[3],
                                )
                            ].id_trend
                            w05_data_new_dict[
                                HashW05Data(
                                    w_new_keys[0],
                                    w_new_keys[1],
                                    w_new_keys[2],
                                    w_new_keys[3],
                                )
                            ].text_value = w05_data_old_dict[
                                HashW05Data(
                                    w_old_keys[0],
                                    w_old_keys[1],
                                    w_old_keys[2],
                                    w_old_keys[3],
                                )
                            ].text_value

            # traslo i w05_classes da ieri
            fine = datetime.datetime.now()
            print(
                "inizio w05_classes di ieri ",
                abs((fine - inizio).total_seconds()),
                "secondi",
            )
            map_time_layouts = {
                "102": "85",
                "98": "81",
                "100": "83",
                "101": "84",
                "99": "82",
                "85": "68",
                "81": "64",
                "83": "66",
                "84": "67",
                "82": "65",
                "68": "51",
                "65": "48",
            }
            for c_old in w05_classes_old_dict:
                c_old_keys = c_old.split(delimiter)
                if c_old_keys[1] in ["PLUV", "TERMA", "FRZLVL", "SNOW_LEV"]:
                    if c_old_keys[3] in map_time_layouts.keys():
                        c_new_keys = c_old.split(delimiter)
                        c_new_keys[3] = map_time_layouts[c_old_keys[3]]
                        w05_classes_new_dict[
                            HashW05Classes(
                                c_new_keys[0],
                                c_new_keys[1],
                                c_new_keys[2],
                                c_new_keys[3],
                                c_new_keys[4],
                            )
                        ].id_classes_value = w05_classes_old_dict[  # type: ignore
                            HashW05Classes(
                                c_old_keys[0],
                                c_old_keys[1],
                                c_old_keys[2],
                                c_old_keys[3],
                                c_old_keys[4],
                            )
                        ].id_classes_value
                        w05_classes_new_dict[
                            HashW05Classes(
                                c_new_keys[0],
                                c_new_keys[1],
                                c_new_keys[2],
                                c_new_keys[3],
                                c_new_keys[4],
                            )
                        ].id_classes = w05_classes_old_dict[  # type: ignore
                            HashW05Classes(
                                c_old_keys[0],
                                c_old_keys[1],
                                c_old_keys[2],
                                c_old_keys[3],
                                c_old_keys[4],
                            )
                        ].id_classes

        # carico i TERMA da weather_values
        fine = datetime.datetime.now()
        print(
            "inizio carica weather_values ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        for w in weather_values_dict:
            w_keys = w.split(delimiter)  # type: ignore
            # carico i dati di temperatura da weather_values
            if w_keys[1] in ["TERMA", "TERMA_1500", "TERMA_700", "TERMA_2000"]:
                if w_keys[0] in [
                    "1",
                    "9",
                    "11",
                    "28",
                    "33",
                    "59",
                    "63",
                    "64",
                    "67",
                ]:  # venue
                    if w_keys[3] in [
                        "33",
                        "50",
                        "51",
                        "67",
                        "68",
                        "84",
                        "85",
                        "101",
                        "102",
                    ]:  # time_layouts
                        if (
                            HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            in w05_data_new_dict
                        ):
                            w05_data_new_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].numeric_value = weather_values_dict[
                                w
                            ].original_numeric_values  # type: ignore
                            w05_data_new_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].id_trend = weather_values_dict[
                                w
                            ].original_trend  # type: ignore
                            w05_data_new_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].text_value = weather_values_dict[
                                w
                            ].original_text_values  # type: ignore

            # carico zero termico da weather_values che è diverso dalla quota neve
            # perchè per esempio la quota neve non ha il trend e ha dei id_time_layouts
            # che non vengono già scritti dalla traslazione iniziale
            if w_keys[1] == "FRZLVL":
                if w_keys[0] in ["67"]:  # venue
                    if w_keys[3] in [
                        "48",
                        "64",
                        "65",
                        "66",
                        "81",
                        "82",
                        "83",
                        "98",
                        "99",
                        "100",
                    ]:  # time_layouts
                        w05_data_new_dict[
                            HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                        ].numeric_value = weather_values_dict[
                            w
                        ].original_numeric_values  # type: ignore
                        w05_data_new_dict[
                            HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                        ].id_trend = weather_values_dict[
                            w
                        ].original_trend  # type: ignore
                        # non sovrascrivo i campi testuali già traslati
                        if (
                            w05_data_new_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].text_value
                            is None
                        ):
                            w05_data_new_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].text_value = weather_values_dict[
                                w
                            ].original_text_values  # type: ignore

            # carico SKY_CONDITION
            if w_keys[1] == "SKY_CONDIT":
                if w_keys[0] in [
                    "1",
                    "9",
                    "11",
                    "28",
                    "33",
                    "59",
                    "63",
                    "64",
                    "87",
                    "88",
                    "89",
                    "90",
                    "91",
                    "92",
                    "93",
                ]:  # venue
                    if w_keys[3] in [
                        "48",
                        "64",
                        "65",
                        "66",
                        "81",
                        "82",
                        "83",
                        "98",
                        "99",
                        "100",
                    ]:  # time_layouts
                        if w_keys[2] in ["912", "913", "914"]:  # aggregazione
                            if (
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                                in w05_data_new_dict
                            ):
                                w05_data_new_dict[
                                    HashW05Data(
                                        w_keys[0], w_keys[1], w_keys[2], w_keys[3]
                                    )
                                ].numeric_value = weather_values_dict[  # type: ignore
                                    w
                                ].original_numeric_values
                                w05_data_new_dict[
                                    HashW05Data(
                                        w_keys[0], w_keys[1], w_keys[2], w_keys[3]
                                    )
                                ].id_trend = weather_values_dict[
                                    w
                                ].original_trend  # type: ignore
                                w05_data_new_dict[
                                    HashW05Data(
                                        w_keys[0], w_keys[1], w_keys[2], w_keys[3]
                                    )
                                ].text_value = weather_values_dict[  # type: ignore
                                    w
                                ].original_text_values
            # carico quota neve
            if w_keys[1] == "SNOW_LEV":
                if w_keys[3] in ["48", "66", "83", "100"]:  # time_layouts
                    w05_data_new_dict[
                        HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                    ].numeric_value = weather_values_dict[
                        w
                    ].original_numeric_values  # type: ignore
                    w05_data_new_dict[
                        HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                    ].id_trend = weather_values_dict[
                        w
                    ].original_trend  # type: ignore
                    w05_data_new_dict[
                        HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                    ].text_value = weather_values_dict[
                        w
                    ].original_text_values  # type: ignore

        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w05_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w05_data_list = []
        for w in w05_data_new_dict:
            w05_data_list.append(w05_data_new_dict[w])
        #     w05_data_new_dict[w].save()
        models.W05Data.objects.bulk_create(w05_data_list)
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w05_classes ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w05_classes_list = []
        for c in w05_classes_new_dict:
            w05_classes_list.append(w05_classes_new_dict[c])
            # w05_classes_new_dict[c].save()
        models.W05Classes.objects.bulk_create(w05_classes_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w05": new.id_w05})

    @action(detail=True, permission_classes=[ReadOnly])
    @atomic
    def data_json(self, request, pk):
        # dato un bollettino completo
        # crea il file di configurazione json per le tabelle w05_data
        inizio = datetime.datetime.now()
        w05_data_json = {}
        my_w05 = models.W05.objects.get(id_w05=pk)
        print(
            "data_json",
            my_w05.id_w05,
            "del",
            my_w05.start_valid_time,
            "iniziato",
        )
        my_05_data = (
            models.W05Data.objects.filter(id_w05=my_w05.id_w05)
            .select_related(
                "id_venue",
                "id_parametro",
                "id_aggregazione",
                "id_trend",
                "id_time_layouts",
            )
            .order_by("id_venue", "id_parametro", "id_aggregazione", "id_time_layouts")
        )
        count = 0
        for d in my_05_data:
            if not (
                d.id_parametro.id_parametro == "SKY_CONDIT"
                and d.id_time_layouts.id_time_layouts in [66, 83, 100]
            ):
                w05_data_tmp = {}
                w05_data_tmp["id_venue"] = d.id_venue.id_venue
                w05_data_tmp["id_parametro"] = d.id_parametro.id_parametro  # type: ignore
                w05_data_tmp["id_aggregazione"] = d.id_aggregazione.id_aggregazione
                w05_data_tmp["id_time_layouts"] = d.id_time_layouts.id_time_layouts
                w05_data_json[count] = w05_data_tmp
                count = count + 1
        fine = datetime.datetime.now()
        print(
            "data_json finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response(w05_data_json)

    @action(detail=True, permission_classes=[ReadOnly])
    @atomic
    def classes_json(self, request, pk):
        # dato un bollettino completo
        # ritorna il file di configurazione json per le tabelle w05_classes
        inizio = datetime.datetime.now()
        w05_classes_json = {}
        my_w05 = models.W05.objects.get(id_w05=pk)
        print(
            "classes_json",
            my_w05.id_w05,
            "del",
            my_w05.start_valid_time,
            "iniziato",
        )
        my_w05_classes = (
            models.W05Classes.objects.filter(id_w05=my_w05.id_w05)
            .select_related(
                "id_venue",
                "id_parametro",
                "id_aggregazione",
                "id_time_layouts",
                "id_classes",
            )
            .order_by(
                "id_venue",
                "id_parametro",
                "id_aggregazione",
                "id_time_layouts",
                "id_classes",
            )
        )
        count = 0
        for c in my_w05_classes:
            w05_classes_tmp = {}
            w05_classes_tmp["id_venue"] = c.id_venue.id_venue
            w05_classes_tmp["id_parametro"] = c.id_parametro.id_parametro  # type: ignore
            w05_classes_tmp["id_aggregazione"] = c.id_aggregazione.id_aggregazione
            w05_classes_tmp["id_time_layouts"] = c.id_time_layouts.id_time_layouts
            w05_classes_tmp["id_classes"] = c.id_classes.id_classes
            w05_classes_json[count] = w05_classes_tmp
            count = count + 1
        fine = datetime.datetime.now()
        print(
            "classes_json finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response(w05_classes_json)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # crea un nuovo bollettino a partire dal bollettino identificato da pk
        # serve per fare una nuova emissione in giornata a causa di errori/modifiche
        delimiter = "__"

        def HashW05Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
            return (
                str(id_venue)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(id_time_layouts)
            )

        def HashW05Classes(
            id_venue, id_parametro, id_aggregazione, id_time_layouts, id_classes
        ):
            return (
                str(id_venue)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(id_time_layouts)
                + delimiter
                + str(id_classes)
            )

        # carico la configurazione json per sapere quanti record ci devono essere su w05_data
        with open("config/w05_data.json") as json_file:
            w05_data_config = json.load(json_file)
        # sistema il json di configurazione in modo da avere come chiave primaria
        # id_venue__id_parametro__id_aggregazione__id_time_layouts
        w05_data_da_inserire = {}  # type: ignore
        for w05_data in w05_data_config:
            w05_data_da_inserire[
                HashW05Data(
                    w05_data_config[w05_data]["id_venue"],
                    w05_data_config[w05_data]["id_parametro"],
                    w05_data_config[w05_data]["id_aggregazione"],
                    w05_data_config[w05_data]["id_time_layouts"],
                )
            ] = None
        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        old = models.W05.objects.get(pk=pk)
        print(
            "reopen del bollettino ",
            old.id_w05,
            "del",
            old.start_valid_time,
            "iniziato",
        )
        old.status = 2
        old.save()

        # aumento il sequenziale perchè è una nuova emissione
        # TODO: genstire il cambio dell'anno
        new_seq = old.seq_num
        if new_seq is not None:
            new_seq = new_seq + 1
        else:
            new_seq = 1
        new = models.W05(
            start_valid_time=old.start_valid_time,
            validity=old.validity,
            next_blt_time=old.next_blt_time,
            situation=old.situation,
            status=0,  # il nuovo bollettino lo metto in bozza
            last_update=inizio,  # aggiornamento ad adesso
            username=request.user,
            seq_num=new_seq,  # incremento il sequenziale
            version=old.version,
            id_w05_parent=old.id_w05,
        )
        new.save()
        old_data = models.W05Data.objects.filter(id_w05=old.id_w05).select_related(
            "id_venue", "id_parametro", "id_aggregazione", "id_trend", "id_time_layouts"
        )
        w05_data_list = []
        for d in old_data:
            # verifico la presenza del w05_data nella configurazione
            if (
                HashW05Data(
                    d.id_venue.id_venue,
                    d.id_parametro.id_parametro,
                    d.id_aggregazione.id_aggregazione,
                    d.id_time_layouts.id_time_layouts,
                )
            ) in w05_data_da_inserire:
                new_data = models.W05Data(
                    id_w05=new,
                    id_venue=d.id_venue,
                    id_parametro=d.id_parametro,
                    id_aggregazione=d.id_aggregazione,
                    numeric_value=d.numeric_value,
                    id_trend=d.id_trend,
                    text_value=d.text_value,
                    id_time_layouts=d.id_time_layouts,
                    start_valid_time=d.start_valid_time,
                    end_valid_time=d.end_valid_time,
                )
                # new_data.save()
                w05_data_list.append(new_data)
                # rimuovo il w05_data inserito
                w05_data_da_inserire.pop(
                    HashW05Data(
                        d.id_venue.id_venue,
                        d.id_parametro.id_parametro,
                        d.id_aggregazione.id_aggregazione,
                        d.id_time_layouts.id_time_layouts,
                    )
                )
        # inserisco i record w05_data mancanti
        # TODO: la get ha pessime performance nel caso manchino parecchi record
        # sarebbe lentissimo occorre escogitare un workaround
        for w05_data in w05_data_da_inserire:
            w05_data_tmp = w05_data.split(delimiter)
            my_time_layouts = models.TimeLayouts.objects.get(pk=w05_data_tmp[3])
            new_data = models.W05Data(
                id_w05=new,
                id_venue=models.Venue.objects.get(pk=w05_data_tmp[0]),
                id_parametro=models.Parametro.objects.get(pk=w05_data_tmp[1]),
                id_aggregazione=models.Aggregazione.objects.get(pk=w05_data_tmp[2]),
                numeric_value=None,
                id_trend=None,
                text_value=None,
                id_time_layouts=my_time_layouts,
                start_valid_time=today
                + datetime.timedelta(days=my_time_layouts.start_day_offset)
                + datetime.timedelta(hours=my_time_layouts.start_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.start_time.minute),
                end_valid_time=today
                + datetime.timedelta(days=my_time_layouts.end_day_offset)  # type: ignore
                + datetime.timedelta(hours=my_time_layouts.end_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.end_time.minute),
            )
            # new_data.save()
            w05_data_list.append(new_data)
        models.W05Data.objects.bulk_create(w05_data_list)

        # carico la configurazione json per sapere quanti record ci devono essere su w05_classes
        with open("config/w05_classes.json") as json_file:
            w05_classes_config = json.load(json_file)
        # sistema il json di configurazione in modo da avere come chiave primaria
        # id_venue__id_parametro__id_aggregazione__id_time_layouts
        w05_classes_da_inserire = {}  # type: ignore
        for w05_classes in w05_classes_config:
            w05_classes_da_inserire[
                HashW05Classes(
                    w05_classes_config[w05_classes]["id_venue"],
                    w05_classes_config[w05_classes]["id_parametro"],
                    w05_classes_config[w05_classes]["id_aggregazione"],
                    w05_classes_config[w05_classes]["id_time_layouts"],
                    w05_classes_config[w05_classes]["id_classes"],
                )
            ] = None
        old_classes = models.W05Classes.objects.filter(
            id_w05=old.id_w05
        ).select_related(
            "id_venue",
            "id_parametro",
            "id_aggregazione",
            "id_classes",
            "id_time_layouts",
        )
        w05_classes_list = []
        for c in old_classes:
            # verifico la presenza del w05_classes nella configurazione
            if (
                HashW05Classes(
                    c.id_venue.id_venue,
                    c.id_parametro.id_parametro,
                    c.id_aggregazione.id_aggregazione,
                    c.id_time_layouts.id_time_layouts,
                    c.id_classes.id_classes,
                )
            ) in w05_classes_da_inserire:
                new_classes = models.W05Classes(
                    id_w05=new,
                    id_venue=c.id_venue,
                    id_parametro=c.id_parametro,
                    id_aggregazione=c.id_aggregazione,
                    id_classes_value=c.id_classes_value,
                    id_classes=c.id_classes,
                    id_time_layouts=c.id_time_layouts,
                    start_valid_time=c.start_valid_time,
                    end_valid_time=c.end_valid_time,
                )
                # new_classes.save()
                w05_classes_list.append(new_classes)
                # rimuovo il w05_classes inserito
                w05_classes_da_inserire.pop(
                    HashW05Classes(
                        c.id_venue.id_venue,
                        c.id_parametro.id_parametro,
                        c.id_aggregazione.id_aggregazione,
                        c.id_time_layouts.id_time_layouts,
                        c.id_classes.id_classes,
                    )
                )
        # inserisco i record w05_classes mancanti
        # TODO: la get ha pessime performance nel caso manchino parecchi record sarebbe
        # lentissimo occorre escogitare un workaround
        for w05_classes in w05_classes_da_inserire:
            w05_classes_tmp = w05_classes.split(delimiter)
            my_time_layouts = models.TimeLayouts.objects.get(pk=w05_classes_tmp[3])
            new_classes = models.W05Classes(
                id_w05=new,
                id_venue=models.Venue.objects.get(pk=w05_classes_tmp[0]),
                id_parametro=models.Parametro.objects.get(pk=w05_classes_tmp[1]),
                id_aggregazione=models.Aggregazione.objects.get(pk=w05_classes_tmp[2]),
                id_classes_value=models.ClassesValue.objects.get(
                    pk=(int(w05_classes_tmp[4]) + 80)
                ),  # è il valore nullo
                id_classes=models.Classes.objects.get(pk=w05_classes_tmp[4]),
                id_time_layouts=my_time_layouts,
                start_valid_time=today
                + datetime.timedelta(days=my_time_layouts.start_day_offset)
                + datetime.timedelta(hours=my_time_layouts.start_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.start_time.minute),
                end_valid_time=today
                + datetime.timedelta(days=my_time_layouts.end_day_offset)  # type: ignore
                + datetime.timedelta(hours=my_time_layouts.end_time.hour)
                + datetime.timedelta(minutes=my_time_layouts.end_time.minute),
            )
            # new_classes.save()
            w05_classes_list.append(new_classes)
        models.W05Classes.objects.bulk_create(w05_classes_list)
        fine = datetime.datetime.now()
        print("reopen finito in ", abs((fine - inizio).total_seconds()), "secondi")
        return Response({"id_w05": new.id_w05})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w05/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w05 = next(s["id"] for s in snapshots if s["id_key"] == "id_w05")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w05",
            "id": id_w05,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w05 = models.W05.objects.get(pk=id_w05)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w05":
                print(
                    "id_w05:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w05, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            elif snapshot["id_key"] == "id_w05_data":
                print(
                    "id_w05_data:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                data = models.W05Data.objects.get(pk=snapshot["id"])
                if snapshot["value_key"] == "id_trend":
                    data.id_trend = models.Trend.objects.get(pk=snapshot["new_value"])
                else:
                    setattr(data, snapshot["value_key"], snapshot["new_value"])
                data.save()
                updated += 1
            elif snapshot["id_key"] == "id_w05_classes":
                print(
                    "id_w05_classes:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                classes = models.W05Classes.objects.get(pk=snapshot["id"])
                if snapshot["value_key"] == "id_classes_value":
                    classes.id_classes_value = models.ClassesValue.objects.get(
                        pk=snapshot["new_value"]
                    )
                else:
                    setattr(classes, snapshot["value_key"], snapshot["new_value"])
                classes.save()
                updated += 1
        w05.save()
        fine = datetime.datetime.now()
        serializer = W05SerializerFull(w05, context={"request": request})
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

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w05 = models.W05.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w05.id_w05,
            "del",
            w05.start_valid_time,
            "iniziato",
        )
        w05.status = "1"
        w05.username = request.user.username
        w05.last_update = inizio
        w05.save()
        # prendi tutti i record di w05_data e copia il valore nei campi validated di weather_values
        w05_data = models.W05Data.objects.filter(id_w05=w05.id_w05).select_related(
            "id_venue", "id_parametro", "id_aggregazione", "id_trend", "id_time_layouts"
        )
        weather_value_list = []
        for d in w05_data:
            data_exists = (
                models.WeatherValues.objects.filter(id_venue=d.id_venue)
                .filter(id_parametro=d.id_parametro)
                .filter(id_aggregazione=d.id_aggregazione)
                .filter(id_time_layouts=d.id_time_layouts)
            )
            for de in data_exists:
                de.validated_numeric_values = d.numeric_value
                de.validated_text_values = d.text_value
                de.validated_trend = d.id_trend
                de.last_update = inizio
                de.username = request.user.username
                # de.save()
                weather_value_list.append(de)
        models.WeatherValues.objects.bulk_update(
            weather_value_list,
            [
                "validated_numeric_values",
                "validated_text_values",
                "validated_trend",
                "last_update",
                "username",
            ],
        )
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("meteo", w05.id_w05)
        return Response({"id_w05": w05.id_w05})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def resend(self, request, pk):
        send_with_celery("meteo", pk)
        print(
            "resend del bollettino ",
            pk,
            "accodato",
        )
        return Response({"id_w05": pk})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reload(self, request, pk):
        # ricarica le temperature
        delimiter = "__"

        def HashW05Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
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
        w05 = models.W05.objects.get(pk=pk)
        print(
            "load_temp del bollettino ",
            w05.id_w05,
            "del",
            w05.start_valid_time,
            "iniziato",
        )
        w05.username = request.user.username
        w05.last_update = inizio
        w05.save()

        w05_data = models.W05Data.objects.filter(id_w05=w05.id_w05).select_related(
            "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
        )
        w05_data_dict = {}
        for w in w05_data:
            w05_data_dict[
                HashW05Data(
                    w.id_venue.id_venue,
                    w.id_parametro.id_parametro,
                    w.id_aggregazione.id_aggregazione,
                    w.id_time_layouts.id_time_layouts,
                )
            ] = w

        weather_values = models.WeatherValues.objects.all().select_related(
            "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
        )
        weather_values_dict = {}
        for w in weather_values:  # type: ignore
            weather_values_dict[
                HashW05Data(
                    w.id_venue.id_venue,
                    w.id_parametro.id_parametro,
                    w.id_aggregazione.id_aggregazione,
                    w.id_time_layouts.id_time_layouts,
                )
            ] = w

        # carico i dati da weather_values
        for w in weather_values_dict:
            w_keys = w.split(delimiter)  # type: ignore
            # carico i dati di temperatura da weather_values
            if w_keys[1] in ["TERMA", "TERMA_1500", "TERMA_700", "TERMA_2000"]:
                if w_keys[0] in [
                    "1",
                    "9",
                    "11",
                    "28",
                    "33",
                    "59",
                    "63",
                    "64",
                    "67",
                ]:  # venue
                    if w_keys[3] in [
                        "33",
                        "50",
                        "51",
                        "67",
                        "68",
                        "84",
                        "85",
                        "101",
                        "102",
                    ]:  # time_layouts
                        if (
                            HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            in w05_data_dict
                        ):
                            w05_data_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].numeric_value = weather_values_dict[
                                w
                            ].original_numeric_values  # type: ignore
                            w05_data_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].id_trend = weather_values_dict[
                                w
                            ].original_trend  # type: ignore
                            w05_data_dict[
                                HashW05Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                            ].text_value = weather_values_dict[
                                w
                            ].original_text_values  # type: ignore

        w_list = []
        for w in w05_data_dict:
            w_list.append(w05_data_dict[w])
            # w05_data_dict[w].save()
        models.W05Data.objects.bulk_update(
            w_list, ["numeric_value", "id_trend", "text_value"]
        )

        fine = datetime.datetime.now()
        print(
            "reload finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w05": w05.id_w05})


class SkyConditionsView(viewsets.ModelViewSet):
    """
    API endpoint that allows W16 bulletins to be viewed or edited
    """

    queryset = models.SkyCondition.objects.all().order_by("sort_index")
    serializer_class = SkyConditionSerializer
    permission_classes = [ReadOnly]


class VenueNamesView(viewsets.ModelViewSet):
    """
    API endpoint that shows city names
    """

    queryset = models.Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [ReadOnly]


class W05ClassesView(viewsets.ModelViewSet):
    """
    API endpoint that allows W05 bulletin Classes to be viewed or edited
    """

    queryset = models.W05Classes.objects.all()
    serializer_class = W05ClassesSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class ClassesView(viewsets.ModelViewSet):
    """
    API endpoint that allows Classes to be viewed
    """

    queryset = models.Classes.objects.all()
    serializer_class = ClassesSerializer
    permission_classes = [ReadOnly]


class W05DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W05 bulletin Data to be viewed or edited
    """

    queryset = models.W05Data.objects.all()
    serializer_class = W05DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


def rearrange(time_layout, key):
    terma_rearranged = {}
    for terma in time_layout[key]:
        terma_rearranged[terma["id_venue"]] = terma
    time_layout[key] = terma_rearranged


def add_icons(sky_condition):
    queryset = models.SkyCondition.objects.all()
    mapping = {}
    for sc in queryset:
        mapping[sc.id_sky_condition] = {
            "description_ita": sc.description_ita,
            "icon": sc.sky_condition,
        }
    for sc in sky_condition:
        nv = int(float(sc["numeric_value"]))  # type: ignore
        sc1 = mapping[nv]
        sc["description_ita"] = sc1["description_ita"]  # type: ignore
        sc["icon"] = sc1["icon"]  # type: ignore


def convert_to_datetime(d, k):
    d[k] = datetime.datetime.strptime(
        d[k].split(".")[0],
        "%Y-%m-%dT%H:%M:%S",
    )


class MeteoSVGView(TemplateView):
    template_name = "meteo.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W05.objects
        w05 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W05SerializerFull(w05)
        meteo = serializer.data
        meteo["logo"] = "meteo_logo"
        convert_to_datetime(meteo, "next_blt_time")
        convert_to_datetime(meteo, "start_valid_time")
        for data in meteo["w05data_set"]:
            convert_to_datetime(data, "start_valid_time")
            if data["id_time_layouts"] not in meteo:
                meteo[data["id_time_layouts"]] = {}
            if data["id_parametro"] in meteo[data["id_time_layouts"]]:
                meteo[data["id_time_layouts"]][data["id_parametro"]].append(data)
            else:
                meteo[data["id_time_layouts"]][data["id_parametro"]] = [data]
        rearrange(meteo[50], "TERMA")
        rearrange(meteo[51], "TERMA")
        rearrange(meteo[67], "TERMA")
        rearrange(meteo[68], "TERMA")
        rearrange(meteo[84], "TERMA")
        rearrange(meteo[85], "TERMA")
        rearrange(meteo[101], "TERMA")
        rearrange(meteo[102], "TERMA")
        rearrange(meteo[48], "SKY_CONDIT")
        rearrange(meteo[64], "SKY_CONDIT")
        rearrange(meteo[65], "SKY_CONDIT")
        rearrange(meteo[81], "SKY_CONDIT")
        rearrange(meteo[82], "SKY_CONDIT")

        del meteo["w05data_set"]

        context = {"meteo": meteo, "title": "Bollettino Meteo"}
        return context


class MeteoPDFView(MeteoSVGView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="meteo.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class PrevisioneSstView(TemplateView):
    template_name = "previsione_sst.txt"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W05.objects
        w05 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W05SerializerFull(w05)
        meteo = serializer.data
        for data in meteo["w05data_set"]:
            convert_to_datetime(data, "start_valid_time")
            if data["id_time_layouts"] not in meteo:
                meteo[data["id_time_layouts"]] = {}
            if data["id_parametro"] in meteo[data["id_time_layouts"]]:
                meteo[data["id_time_layouts"]][data["id_parametro"]].append(data)
            else:
                meteo[data["id_time_layouts"]][data["id_parametro"]] = [data]
        for id_time_layout in [48, 66, 83, 100]:
            rearrange(meteo[id_time_layout], "COP_TOT")
            rearrange(meteo[id_time_layout], "PLUV")
            rearrange(meteo[id_time_layout], "FRZLVL")
            rearrange(meteo[id_time_layout], "VELV")
        context = {"meteo": meteo}
        return context


class MeteoXmlView(TemplateView):
    template_name = "meteo.xml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W05.objects
        w05 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W05SerializerFull(w05)
        meteo = serializer.data
        convert_to_datetime(meteo, "last_update")
        convert_to_datetime(meteo, "start_valid_time")
        convert_to_datetime(meteo, "next_blt_time")
        for data in meteo["w05data_set"]:
            convert_to_datetime(data, "start_valid_time")
            convert_to_datetime(data, "end_valid_time")
            if data["id_time_layouts"] not in meteo:
                meteo[data["id_time_layouts"]] = {}
            if data["id_parametro"] in meteo[data["id_time_layouts"]]:
                meteo[data["id_time_layouts"]][data["id_parametro"]].append(data)
            else:
                meteo[data["id_time_layouts"]][data["id_parametro"]] = [data]
        for id_time_layout in [48, 66, 83, 100]:
            rearrange(meteo[id_time_layout], "COP_TOT")
            rearrange(meteo[id_time_layout], "PLUV")
            rearrange(meteo[id_time_layout], "FRZLVL")
            rearrange(meteo[id_time_layout], "VELV")
            rearrange(meteo[id_time_layout], "WFR")
            rearrange(meteo[id_time_layout], "WFOP")
        for id_time_layout in [48, 64, 65, 81, 82, 98, 99]:
            add_icons(meteo[id_time_layout]["SKY_CONDIT"])
            rearrange(meteo[id_time_layout], "SKY_CONDIT")
        for id_time_layout in [50, 51, 67, 68, 84, 85, 101, 102]:
            rearrange(meteo[id_time_layout], "TERMA")
            rearrange(meteo[id_time_layout], "TERMA_700")
            rearrange(meteo[id_time_layout], "TERMA_1500")
            rearrange(meteo[id_time_layout], "TERMA_2000")
        meteo["semigiorni"] = [
            copy.deepcopy(meteo[48]),
            copy.deepcopy(meteo[66]),
            copy.deepcopy(meteo[66]),
            copy.deepcopy(meteo[83]),
            copy.deepcopy(meteo[83]),
            copy.deepcopy(meteo[100]),
            copy.deepcopy(meteo[100]),
        ]

        meteo["semigiorni"][0]["MASSIME"] = meteo[50]
        meteo["semigiorni"][0]["MINIME"] = meteo[51]

        meteo["semigiorni"][1]["MASSIME"] = meteo[67]
        meteo["semigiorni"][1]["MINIME"] = meteo[68]
        meteo["semigiorni"][1]["SKY_CONDIT"] = meteo[64]["SKY_CONDIT"]

        meteo["semigiorni"][2]["MASSIME"] = meteo[67]
        meteo["semigiorni"][2]["MINIME"] = meteo[68]
        meteo["semigiorni"][2]["SKY_CONDIT"] = meteo[65]["SKY_CONDIT"]

        meteo["semigiorni"][3]["MASSIME"] = meteo[84]
        meteo["semigiorni"][3]["MINIME"] = meteo[85]
        meteo["semigiorni"][3]["SKY_CONDIT"] = meteo[81]["SKY_CONDIT"]

        meteo["semigiorni"][4]["MASSIME"] = meteo[84]
        meteo["semigiorni"][4]["MINIME"] = meteo[85]
        meteo["semigiorni"][4]["SKY_CONDIT"] = meteo[82]["SKY_CONDIT"]

        meteo["semigiorni"][5]["MASSIME"] = meteo[101]
        meteo["semigiorni"][5]["MINIME"] = meteo[102]
        meteo["semigiorni"][5]["SKY_CONDIT"] = meteo[98]["SKY_CONDIT"]

        meteo["semigiorni"][6]["MASSIME"] = meteo[101]
        meteo["semigiorni"][6]["MINIME"] = meteo[102]
        meteo["semigiorni"][6]["SKY_CONDIT"] = meteo[99]["SKY_CONDIT"]

        context = {"meteo": meteo}
        return context


class MeteoBmpView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w05/pdf/%d" % kwargs["pk"])

        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(r.content)
            f.flush()
            bmp_name = "%s.bmp" % f.name
            command = "convert -verbose -density 145 -crop 1191x1685+3x5 %s %s" % (
                f.name,
                bmp_name,
            )
            retcode = call(command, shell=True)
            if retcode != 0:
                error = "imagemagick convert failed with code: %d" % retcode
                raise Exception(error)
            with open(bmp_name, mode="rb") as bmp_file:
                bmp_content = bmp_file.read()
            os.remove(bmp_name)
            return HttpResponse(
                content=memoryview(bmp_content), content_type="image/bmp"
            )


class MeteoPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w05/pdf/%d" % kwargs["pk"])

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


class MeteoWebarpaView(TemplateView):
    template_name = "webarpa.xml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W05.objects
        w05 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W05SerializerFull(w05)
        meteo = serializer.data
        for data in meteo["w05data_set"]:
            convert_to_datetime(data, "start_valid_time")
            if data["id_time_layouts"] not in meteo:
                meteo[data["id_time_layouts"]] = {}
            if data["id_parametro"] in meteo[data["id_time_layouts"]]:
                meteo[data["id_time_layouts"]][data["id_parametro"]].append(data)
            else:
                meteo[data["id_time_layouts"]][data["id_parametro"]] = [data]
        for id_time_layout in [48, 64, 65, 81, 82]:
            rearrange(meteo[id_time_layout], "SKY_CONDIT")
        for id_time_layout in [48, 66, 83]:
            rearrange(meteo[id_time_layout], "COP_TOT")
            rearrange(meteo[id_time_layout], "PLUV")
            rearrange(meteo[id_time_layout], "FRZLVL")
            rearrange(meteo[id_time_layout], "VELV")
        meteo[48]["ampm"] = "pomeriggio"
        meteo[64]["ampm"] = "mattino"
        meteo[64]["COP_TOT"] = meteo[66]["COP_TOT"]
        meteo[64]["PLUV"] = meteo[66]["PLUV"]
        meteo[64]["FRZLVL"] = meteo[66]["FRZLVL"]
        meteo[64]["VELV"] = meteo[66]["VELV"]
        meteo[65]["ampm"] = "pomeriggio"
        meteo[65]["COP_TOT"] = meteo[66]["COP_TOT"]
        meteo[65]["PLUV"] = meteo[66]["PLUV"]
        meteo[65]["FRZLVL"] = meteo[66]["FRZLVL"]
        meteo[65]["VELV"] = meteo[66]["VELV"]
        meteo[81]["ampm"] = "mattino"
        meteo[81]["COP_TOT"] = meteo[83]["COP_TOT"]
        meteo[81]["PLUV"] = meteo[83]["PLUV"]
        meteo[81]["FRZLVL"] = meteo[83]["FRZLVL"]
        meteo[81]["VELV"] = meteo[83]["VELV"]
        meteo[82]["ampm"] = "pomeriggio"
        meteo[82]["COP_TOT"] = meteo[83]["COP_TOT"]
        meteo[82]["PLUV"] = meteo[83]["PLUV"]
        meteo[82]["FRZLVL"] = meteo[83]["FRZLVL"]
        meteo[82]["VELV"] = meteo[83]["VELV"]
        for id_time_layout in [50, 51, 67, 68, 84, 85]:
            rearrange(meteo[id_time_layout], "TERMA")
        meteo["semigiorni"] = [meteo[48], meteo[64], meteo[65], meteo[81], meteo[82]]
        meteo["semigiorni"][0]["MASSIME"] = meteo[50]
        meteo["semigiorni"][1]["MASSIME"] = meteo[67]
        meteo["semigiorni"][1]["MINIME"] = meteo[68]
        meteo["semigiorni"][2]["MASSIME"] = meteo[67]
        meteo["semigiorni"][2]["MINIME"] = meteo[68]
        meteo["semigiorni"][3]["MASSIME"] = meteo[84]
        meteo["semigiorni"][3]["MINIME"] = meteo[85]
        meteo["semigiorni"][4]["MASSIME"] = meteo[84]
        meteo["semigiorni"][4]["MINIME"] = meteo[85]
        context = {"meteo": meteo}
        return context


class MeteoWebarpaOldView(MeteoWebarpaView):
    template_name = "webarpa_old.xml"
