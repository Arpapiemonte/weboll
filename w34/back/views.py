#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
import locale
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

from w34.back import models
from w34.back.serializers import W34DataSerializer, W34Serializer, W34SerializerFull
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core import models as models_w05


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W34View(viewsets.ModelViewSet):
    """
    API endpoint that allows W34 bulletins to be viewed or edited
    """

    queryset = models.W34.objects.order_by("-last_update", "-pk")
    serializer_class = W34Serializer
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
        queryset = models.W34.objects
        if (
            instance.id_w34_parent
            and queryset.filter(pk=instance.id_w34_parent).exists()
        ):
            w34 = get_object_or_404(queryset, pk=instance.id_w34_parent)
            w34.status = "1"
            if not User.objects.filter(username=w34.username).exists():
                print("perform_destroy non trovo l'utente " + w34.username)
                w34.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w34.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W34.objects
        w34 = get_object_or_404(queryset, pk=pk)
        serializer = W34SerializerFull(w34, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w34 = models.W34.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w34.id_w34,
            "del",
            w34.data_emissione,
            "iniziato",
        )
        w34.status = "1"
        w34.username = request.user.username
        w34.last_update = inizio
        w34.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("corriere_novara", w34.id_w34)
        return Response({"id_w34": w34.id_w34})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # delimiter_firstguess = ";"
        delimiter = "__"

        def HashW34Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
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
        # tomorrow = emissione + datetime.timedelta(days=1)
        # today_bulletins = models.W34.objects.filter(data_emissione=today.date()).count()
        # if today_bulletins >= 1:
        #     raise ExistingTodayBulletin()
        old_w34 = None
        if (
            models.W34.objects.filter(status="1")
            .filter(data_emissione__year=today.year)
            .order_by("-last_update")
            .exists()
        ):
            old_w34 = (
                models.W34.objects.filter(status="1")
                .filter(data_emissione__year=today.year)
                .order_by("-last_update")
                .latest("pk")
            )
        if old_w34 is not None:
            print(
                "new del bollettino ",
                old_w34.id_w34,
                "del",
                old_w34.data_emissione,
                "iniziato",
            )
            # aumento il sequenziale perchè è una nuova emissione
            seq_num = int(old_w34.seq_num)  # type: ignore
            seq_num = seq_num + 1
        else:
            seq_num = 1

        new_w05 = None
        new_w05 = (
            models_w05.W05.objects.filter(status="1")
            .filter(start_valid_time__year=today.year)
            .filter(start_valid_time__month=today.month)
            .filter(start_valid_time__day=today.day)
            .count()
        )

        if new_w05 > 0:
            # print("old_w34", old_w34)
            new = models.W34(
                data_emissione=emissione.date(),
                status=0,
                last_update=datetime.datetime.now(),
                username=request.user,
                seq_num=str(seq_num),
            )
            new.save()

            # zone = models.Venue.objects.all()
            # zone_dict = {}
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
            # print(aggregazione_dict)

            # Temperature di Novara e Verbania da w05
            novara_d0_max = 0
            novara_d1_max = 0
            novara_d2_max = 0
            novara_d0_min = 0
            novara_d1_min = 0
            novara_d2_min = 0
            verbania_d0_max = 0
            verbania_d1_max = 0
            verbania_d2_max = 0
            verbania_d0_min = 0
            verbania_d1_min = 0
            verbania_d2_min = 0
            news_w05 = None
            news_w05 = (
                models_w05.W05.objects.filter(status="1")
                .filter(start_valid_time__year=today.year)
                .filter(start_valid_time__month=today.month)
                .filter(start_valid_time__day=today.day)
                .latest("pk")
            )
            id_w05_value = None
            id_w05_value = news_w05.id_w05

            new_w05_data_no = None
            new_w05_data_no = (
                models_w05.W05Data.objects.filter(id_w05=id_w05_value)  # type: ignore
                .filter(id_parametro="TERMA")
                .filter(id_venue="33")
            )

            new_w05_data_vb = None
            new_w05_data_vb = (
                models_w05.W05Data.objects.filter(id_w05=id_w05_value)  # type: ignore
                .filter(id_parametro="TERMA")
                .filter(id_venue="63")
            )

            novara_value = 0
            for value_data in new_w05_data_no:
                novara_value = value_data.numeric_value  # type: ignore
                novara_td = value_data.id_time_layouts
                novara_aggr = value_data.id_aggregazione
                if (
                    novara_aggr == aggregazione_dict[str(328)]
                    and novara_td == time_layouts_dict[str(67)]
                ):
                    novara_d0_max = int(novara_value)
                if (
                    novara_aggr == aggregazione_dict[str(327)]
                    and novara_td == time_layouts_dict[str(68)]
                ):
                    novara_d0_min = int(novara_value)
                if (
                    novara_aggr == aggregazione_dict[str(328)]
                    and novara_td == time_layouts_dict[str(84)]
                ):
                    novara_d1_max = int(novara_value)
                if (
                    novara_aggr == aggregazione_dict[str(327)]
                    and novara_td == time_layouts_dict[str(85)]
                ):
                    novara_d1_min = int(novara_value)
                if (
                    novara_aggr == aggregazione_dict[str(328)]
                    and novara_td == time_layouts_dict[str(101)]
                ):
                    novara_d2_max = int(novara_value)
                if (
                    novara_aggr == aggregazione_dict[str(327)]
                    and novara_td == time_layouts_dict[str(102)]
                ):
                    novara_d2_min = int(novara_value)

            verbania_value = 0
            for value_data in new_w05_data_vb:
                verbania_value = value_data.numeric_value  # type: ignore
                verbania_td = value_data.id_time_layouts
                verbania_aggr = value_data.id_aggregazione
                if (
                    verbania_aggr == aggregazione_dict[str(328)]
                    and verbania_td == time_layouts_dict[str(67)]
                ):
                    verbania_d0_max = int(verbania_value)
                if (
                    verbania_aggr == aggregazione_dict[str(327)]
                    and verbania_td == time_layouts_dict[str(68)]
                ):
                    verbania_d0_min = int(verbania_value)
                if (
                    verbania_aggr == aggregazione_dict[str(328)]
                    and verbania_td == time_layouts_dict[str(84)]
                ):
                    verbania_d1_max = int(verbania_value)
                if (
                    verbania_aggr == aggregazione_dict[str(327)]
                    and verbania_td == time_layouts_dict[str(85)]
                ):
                    verbania_d1_min = int(verbania_value)
                if (
                    verbania_aggr == aggregazione_dict[str(328)]
                    and verbania_td == time_layouts_dict[str(101)]
                ):
                    verbania_d2_max = int(verbania_value)
                if (
                    verbania_aggr == aggregazione_dict[str(327)]
                    and verbania_td == time_layouts_dict[str(102)]
                ):
                    verbania_d2_min = int(verbania_value)

            parametri = models_w05.Parametro.objects.all()
            parametri_dict = {}
            for p in parametri:
                parametri_dict[p.id_parametro] = p

            # riempo il dizionario con i dati del json di default
            w34_data_new_dict = {}  # type: ignore

            weather_values = models_w05.WeatherValues.objects.all().select_related(
                "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
            )

            weather_values_dict = {}
            for w in weather_values:
                weather_values_dict[
                    HashW34Data(
                        w.id_venue.id_venue,
                        w.id_parametro.id_parametro,
                        w.id_aggregazione.id_aggregazione,
                        w.id_time_layouts.id_time_layouts,
                    )
                ] = w

            # carico la configurazione json per sapere quanti record ci devono essere su w05_data
            with open("config/w34_data.json") as json_file:
                w34_data_config = json.load(json_file)

            w34_data_new_dict = {}
            for w34 in w34_data_config:
                w34_data_new_dict[
                    HashW34Data(
                        w34["id_venue"],
                        w34["id_parametro"],
                        w34["id_aggregazione"],
                        w34["id_time_layouts"],
                    )
                ] = models.W34Data(
                    id_w34=new,
                    id_venue=int(w34["id_venue"]),
                    id_parametro=parametri_dict[w34["id_parametro"]],
                    id_aggregazione=aggregazione_dict[str(w34["id_aggregazione"])],
                    id_time_layouts=time_layouts_dict[str(w34["id_time_layouts"])],
                    numeric_value=None,
                )
                if (
                    HashW34Data(
                        w34["id_venue"],
                        w34["id_parametro"],
                        w34["id_aggregazione"],
                        w34["id_time_layouts"],
                    )
                    in weather_values_dict
                ):
                    w34_data_new_dict[
                        HashW34Data(
                            w34["id_venue"],
                            w34["id_parametro"],
                            w34["id_aggregazione"],
                            w34["id_time_layouts"],
                        )
                    ] = weather_values_dict[  # type: ignore
                        HashW34Data(
                            w34["id_venue"],
                            w34["id_parametro"],
                            w34["id_aggregazione"],
                            w34["id_time_layouts"],
                        )
                    ]

            fine = datetime.datetime.now()
            print(
                "inizio salvataggioin w34_data ",
                abs((fine - inizio).total_seconds()),
                "secondi",
            )

            w34_data_list = []
            for w34d in w34_data_new_dict:
                if type(w34_data_new_dict[w34d]) is models_w05.WeatherValues:
                    w34_data_record = models.W34Data(
                        id_w34=new,
                        id_venue=w34_data_new_dict[w34d].id_venue.id_venue,  # type: ignore
                        id_parametro=w34_data_new_dict[w34d].id_parametro,
                        id_aggregazione=w34_data_new_dict[w34d].id_aggregazione,
                        id_time_layouts=w34_data_new_dict[w34d].id_time_layouts,
                        numeric_value=w34_data_new_dict[w34d].original_numeric_values,  # type: ignore
                    )
                    if (
                        w34_data_new_dict[w34d].id_venue.id_venue != 33  # type: ignore
                        and w34_data_new_dict[w34d].id_venue.id_venue != 63  # type: ignore
                    ):
                        w34_data_list.append(w34_data_record)
                    else:
                        if w34_data_new_dict[w34d].id_venue.id_venue == 33:  # type: ignore
                            # NOVARA
                            if (
                                w34_data_new_dict[w34d].id_aggregazione.id_aggregazione
                                == 328
                            ):
                                # MAX
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 67
                                ):
                                    print("NOVARA W05 MAX D0")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=33,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=novara_d0_max,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 84
                                ):
                                    print("NOVARA W05 MAX D1")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=33,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=novara_d1_max,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 101
                                ):
                                    print("NOVARA W05 MAX D2")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=33,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=novara_d2_max,
                                    )
                            elif (
                                w34_data_new_dict[w34d].id_aggregazione.id_aggregazione
                                == 327
                            ):
                                # MIN
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 68
                                ):
                                    print("NOVARA W05 MIN D0")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=33,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=novara_d0_min,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 85
                                ):
                                    print("NOVARA W05 MIN D1")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=33,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=novara_d1_min,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 102
                                ):
                                    print("NOVARA W05 MIN D2")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=33,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=novara_d2_min,
                                    )
                        elif w34_data_new_dict[w34d].id_venue.id_venue == 63:  # type: ignore
                            # VERBANIA
                            if (
                                w34_data_new_dict[w34d].id_aggregazione.id_aggregazione
                                == 328
                            ):
                                # MAX
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 67
                                ):
                                    print("VERBANIA W05 MAX D0")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=63,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=verbania_d0_max,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 84
                                ):
                                    print("VERBANIA W05 MAX D1")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=63,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=verbania_d1_max,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 101
                                ):
                                    print("VERBANIA W05 MAX D2")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=63,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=verbania_d2_max,
                                    )
                            elif (
                                w34_data_new_dict[w34d].id_aggregazione.id_aggregazione
                                == 327
                            ):
                                # MIN
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 68
                                ):
                                    print("VERBANIA W05 MIN D0")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=63,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=verbania_d0_min,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 85
                                ):
                                    print("VERBANIA W05 MIN D1")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=63,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=verbania_d1_min,
                                    )
                                if (
                                    w34_data_new_dict[
                                        w34d
                                    ].id_time_layouts.id_time_layouts
                                    == 102
                                ):
                                    print("VERBANIA W05 MIN D2")
                                    w34_data_record = models.W34Data(
                                        id_w34=new,
                                        id_venue=63,
                                        id_parametro=w34_data_new_dict[
                                            w34d
                                        ].id_parametro,
                                        id_aggregazione=w34_data_new_dict[
                                            w34d
                                        ].id_aggregazione,
                                        id_time_layouts=w34_data_new_dict[
                                            w34d
                                        ].id_time_layouts,
                                        numeric_value=verbania_d2_min,
                                    )
                        w34_data_list.append(w34_data_record)
            models.W34Data.objects.bulk_create(w34_data_list)
            fine = datetime.datetime.now()
            print(
                "new finito in ",
                abs((fine - inizio).total_seconds()),
                "secondi",
            )
            return Response({"id_w34": new.id_w34})
        else:
            str_error = "Non trovo bollettino meteo di OGGI"
            print(str_error)
            return Response(data={"error": str_error}, status=555)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W34.objects.get(pk=pk)
        print("w34 reopen:", old)
        old.status = "2"
        old_id_w34 = old.id_w34
        old.save()
        seq_num = int(old.seq_num)  # type: ignore
        seq_num = seq_num + 1
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w34_parent = old_id_w34
        new.seq_num = seq_num
        new.save()
        # print('created: ', new)
        old_data = models.W34Data.objects.filter(id_w34=old_id_w34)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w34 = new
            new_data.save()

        return Response({"id_w34": new.id_w34})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w34/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w34 = snapshots["id_w34"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w34 = models.W34.objects.get(pk=id_w34)
        for snapshot in snapshots:
            setattr(w34, snapshot, snapshots[snapshot])
        w34.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W34SerializerFull(w34, context={"request": request})
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


class W34DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W34 bulletin Data to be viewed or edited
    """

    queryset = models.W34Data.objects.all()
    serializer_class = W34DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W34Data.objects
        w34Data = get_object_or_404(queryset, pk=pk)
        serializer = W34DataSerializer(w34Data, context={"request": request})
        return Response(serializer.data)


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%dT%H:%M:%S",
    )


class CorriereHTMLView(TemplateView):
    template_name = "corriere.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W34.objects
        w34 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W34SerializerFull(w34)
        corriere = serializer.data
        corriere_rearranged = {}  # type: ignore
        for data in corriere["w34data_set"]:
            if data["id_aggregazione"] not in corriere_rearranged:
                corriere_rearranged[data["id_aggregazione"]] = {}
            if (
                data["id_time_layouts"]
                not in corriere_rearranged[data["id_aggregazione"]]
            ):
                corriere_rearranged[data["id_aggregazione"]][
                    data["id_time_layouts"]
                ] = {}
            if data["id_venue"] not in corriere_rearranged[data["id_aggregazione"]]:
                corriere_rearranged[data["id_aggregazione"]][data["id_time_layouts"]][
                    data["id_venue"]
                ] = {}
            corriere_rearranged[data["id_aggregazione"]][data["id_time_layouts"]][
                data["id_venue"]
            ] = data["numeric_value"]
        locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")
        date_d1 = (
            datetime.datetime.strptime(corriere["data_emissione"][0:10], "%Y-%m-%d")
            + datetime.timedelta(days=1)
        ).strftime("%A %d %B %Y")
        date_d2 = (
            datetime.datetime.strptime(corriere["data_emissione"][0:10], "%Y-%m-%d")
            + datetime.timedelta(days=2)
        ).strftime("%A %d %B %Y")
        date_d3 = (
            datetime.datetime.strptime(corriere["data_emissione"][0:10], "%Y-%m-%d")
            + datetime.timedelta(days=3)
        ).strftime("%A %d %B %Y")
        convert_to_date(corriere, "data_emissione")
        print("date_d1", date_d1)
        print("date_d1", date_d2)
        print("date_d1", date_d3)
        context = {
            "date_d1": date_d1,
            "date_d2": date_d2,
            "date_d3": date_d3,
            "corriere": corriere,
            "title": "Bollettino Corriere Novara",
            "corriere_arra": corriere_rearranged,
        }
        return context


class CorrierePDFView(CorriereHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="corriere.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class CorrierePngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w34/pdf/%d" % kwargs["pk"])

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
