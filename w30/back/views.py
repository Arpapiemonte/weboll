#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
# import copy
import datetime
import json
from html.parser import HTMLParser
from os import getenv
from os.path import splitext

import requests
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from w30.back import models
from w30.back.serializers import (
    W30CurrentDataViewSerializer,
    W30DataSerializer,
    W30Serializer,
    W30SerializerFull,
)
from website.common.tasks import send_with_celery
from website.common.views import BulletinDraftLocked, StandardResultsSetPagination

# import os
# import tempfile
# from subprocess import call


class MyHTMLParser(HTMLParser):
    files = []  # type: ignore

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href":
                    href = attr[1]
                    parts = splitext(href)
                    ext = parts[1]
                    if ext == ".json":
                        name = parts[0]
                        self.files.append(name)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W30View(viewsets.ModelViewSet):
    """
    API endpoint that allows W30 bulletins to be viewed or edited
    """

    queryset = models.W30.objects.order_by("-last_update", "-pk")
    serializer_class = W30Serializer
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
        queryset = models.W30.objects
        W30 = get_object_or_404(queryset, pk=pk)
        serializer = W30SerializerFull(W30, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W30.objects
        if (
            instance.id_w30_parent
            and queryset.filter(pk=instance.id_w30_parent).exists()
        ):
            w30 = get_object_or_404(queryset, pk=instance.id_w30_parent)
            w30.status = "1"
            if not User.objects.filter(username=w30.username).exists():
                print("perform_destroy non trovo l'utente " + w30.username)
                w30.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w30.save()
        instance.delete()

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # crea il nuovo bollettino di oggi
        print("w30 new")
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        emissione = today.replace(hour=12, minute=30, second=0, microsecond=0)
        data_prossimo_aggiornamento = emissione + datetime.timedelta(days=1)

        old_queryset = models.W30.objects.filter(status="1").order_by("-last_update")

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
                    models.W30.objects.filter(data_emissione__year=today.year)
                    .exclude(status="0")
                    .latest("seq_num")
                    .seq_num
                )
                last_seq_num = last_seq_num if last_seq_num is not None else 0
                new_seq = last_seq_num + 1
        else:
            print("primo bollettino")
            new_seq = 1

        parser = MyHTMLParser()
        url = getenv("BASE_DATA_URL_FULL", "http://frontend:80")
        if url == "http://frontend:80":
            url += "/models_for_psa/index.html"
        else:
            url += "/models_for_psa/"
        with requests.get(url) as r:
            html = r.content.decode()
        parser.feed(html)

        if len(parser.files) == 0:
            error = "No model JSON file found"
            raise Exception(error)

        noecmwf = False
        firstguess = ""
        if "ECMWF0100_00_D0" in parser.files:
            firstguess = "ECMWF0100_00_D0"
        elif "ECMWF0100_12_D1" in parser.files:
            firstguess = "ECMWF0100_12_D1"
        else:
            noecmwf = True

        if noecmwf:
            f = open("config/MODEL.json")
            eumodel = json.load(f)
        else:
            url = f"{getenv('BASE_DATA_URL_FULL', 'http://frontend:80')}/models_for_psa/{firstguess}.json"
            with requests.get(url) as r:
                if r.status_code == 200:
                    eumodel = json.loads(r.content)
                else:
                    f = open("config/MODEL.json")
                    eumodel = json.load(f)

        timeLayouts = [43, 44, 45, 46, 60, 61, 62, 63, 77, 78, 79, 80]
        euvalues = []

        i = 0

        for datiArea in eumodel["data"]:
            i = 0
            for timelayout in timeLayouts:
                data900 = {
                    "id_aggregazione": 900,
                    "id_allertamento": datiArea["area_allertamento"],
                    "id_parametro": "PLUV",
                    "id_time_layouts": timelayout,
                    "numeric_value": datiArea["PLUV"]["900"][i],
                }

                data125 = {
                    "id_aggregazione": 125,
                    "id_allertamento": datiArea["area_allertamento"],
                    "id_parametro": "PLUV",
                    "id_time_layouts": timelayout,
                    "numeric_value": datiArea["PLUV"]["125"][i],
                }

                dataSnow = {
                    "id_aggregazione": 0,
                    "id_allertamento": datiArea["area_allertamento"],
                    "id_parametro": "SNOW_LEV",
                    "id_time_layouts": timelayout,
                    "numeric_value": datiArea["SNOW_LEV"]["0"][i],
                }

                dataFreeze = {
                    "id_aggregazione": 0,
                    "id_allertamento": datiArea["area_allertamento"],
                    "id_parametro": "FRZLVL",
                    "id_time_layouts": timelayout,
                    "numeric_value": datiArea["FRZLVL"]["0"][i],
                }

                euvalues.append(data900)
                euvalues.append(data125)
                euvalues.append(dataSnow)
                euvalues.append(dataFreeze)
                i += 1

        new = models.W30(
            data_emissione=emissione,  # devono essere le 12:30
            data_prossimo_aggiornamento=data_prossimo_aggiornamento,
            status="0",  # il nuovo bollettino lo metto in bozza
            last_update=now,
            username=request.user,
            seq_num=new_seq,  # incremento il sequenziale
            firstguess=f"Model: {eumodel['model']} Date: {eumodel['date']} Run: {eumodel['run']}",
        )
        new.save()
        print("created: ", new)

        areeAllertamento = models.AreeAllertamento.objects.all()
        areeAllertamento_dict = {}
        for m in areeAllertamento:
            areeAllertamento_dict[str(m.id_allertamento)] = m

        aggregazione = models.Aggregazione.objects.all()
        aggregazione_dict = {}
        for mm in aggregazione:
            aggregazione_dict[str(mm.id_aggregazione)] = mm

        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for mmm in time_layouts:
            time_layouts_dict[mmm.id_time_layouts] = mmm

        parametro = models.Parametro.objects.all().select_related("id_unita_misura")
        parametro_dict = {}
        for mmmm in parametro:
            parametro_dict[mmmm.id_parametro] = mmmm

        with open("config/w30_data.json") as json_file:
            w30_data_config = json.load(json_file)

        for data in w30_data_config:
            new_data = models.W30Data(
                id_w30=new,
                id_aggregazione=aggregazione_dict[data["id_aggregazione"]],
                id_allertamento=areeAllertamento_dict[data["id_allertamento"]],
                id_parametro=parametro_dict[data["id_parametro"]],
                id_time_layouts=time_layouts_dict[data["id_time_layouts"]],
                numeric_value=None,
            )
            new_data.pk = None
            for eudata in euvalues:
                if (
                    eudata["id_aggregazione"] == new_data.id_aggregazione.pk
                    and eudata["id_allertamento"] == new_data.id_allertamento.pk
                    and eudata["id_parametro"] == new_data.id_parametro.pk
                    and eudata["id_time_layouts"] == new_data.id_time_layouts.pk
                ):
                    new_data.numeric_value = eudata["numeric_value"]
            new_data.save()

        return Response({"id_w30": new.id_w30})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W30.objects.get(pk=pk)
        print("w30 reopen:", old)
        old.status = "2"
        old_id_w30 = old.id_w30
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
        new.id_w30_parent = old_id_w30
        new.save()
        # print('created: ', new)
        old_data = (
            models.W30Data.objects.filter(id_w30=old_id_w30)
            .exclude(id_aggregazione=901)
            .exclude(id_aggregazione=902)
            .exclude(id_aggregazione=903)
        )
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w30 = new
            new_data.save()

        return Response({"id_w30": new.id_w30})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w30 = models.W30.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w30.id_w30,
            "del",
            w30.data_emissione,
            "iniziato",
        )
        w30.status = "1"
        w30.username = request.user.username
        w30.last_update = inizio
        w30.save()

        print(
            "Calcolo aggregazioni 901, 902, 903...",
        )

        areeAllertamento = models.AreeAllertamento.objects.all()
        areeAllertamento_dict = {}
        for m in areeAllertamento:
            areeAllertamento_dict[str(m.id_allertamento)] = m

        aggregazione = models.Aggregazione.objects.all()
        aggregazione_dict = {}
        for mm in aggregazione:
            aggregazione_dict[str(mm.id_aggregazione)] = mm

        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for mmm in time_layouts:
            time_layouts_dict[mmm.id_time_layouts] = mmm

        parametro = models.Parametro.objects.all().select_related("id_unita_misura")
        parametro_dict = {}
        for mmmm in parametro:
            parametro_dict[mmmm.id_parametro] = mmmm

        today = datetime.datetime.today()
        data_emissione = today.replace(hour=12, minute=0, second=0, microsecond=0)

        old_forecast_zone = models.ForecastZone.objects.filter(
            data_emissione=data_emissione
        ).filter(model_name="PSA_00_DO")

        old_forecast_zone.delete()
        print("==============ELIMINAZIONE VECCHI DATI============")
        start = today.replace(hour=12, minute=0, second=0, microsecond=0)

        psa_time_layouts = [45, 46, 48, 60, 61, 62, 63, 66, 77, 78, 79, 80]

        date_riferimento = {}
        for psa_tl in psa_time_layouts:
            time_layout = time_layouts_dict[psa_tl]
            offset = time_layout.start_day_offset
            end_time = datetime.datetime.strptime(
                time_layout.end_time.strftime("%H/%M/%S"), "%H/%M/%S"
            )
            end_time = end_time.replace(
                year=start.year, month=start.month, day=start.day
            )
            end_time = (
                end_time
                + datetime.timedelta(seconds=1)
                + datetime.timedelta(days=offset)
            )
            date_riferimento[str(psa_tl)] = end_time

        allW30Data = (
            models.W30Data.objects.filter(id_w30=w30.id_w30)
            .exclude(id_time_layouts="43")
            .exclude(id_time_layouts="44")
        )  # Skip the first two time_layouts

        for w30data in allW30Data:
            newforecastzone = models.ForecastZone(
                id_allertamento=w30data.id_allertamento,
                id_parametro=w30data.id_parametro,
                id_aggregazione=w30data.id_aggregazione,
                model_type="DMO",
                model_name="PSA_00_DO",
                data_emissione=data_emissione,
                data_riferimento=date_riferimento[
                    str(w30data.id_time_layouts.id_time_layouts)
                ],
                valore_originale=w30data.numeric_value,
                valore_validato=None,
                last_update=inizio,
                username=request.user.username,
            )
            newforecastzone.save()

        psa_time_layouts6h = [45, 46, 60, 61, 62, 63, 77, 78, 79, 80]

        medieArray = []
        for psa_tl in psa_time_layouts6h:
            mediaTL = (
                models.W30Data.objects.filter(id_w30=w30.id_w30)
                .filter(id_aggregazione=900)
                .filter(id_time_layouts=psa_tl)
                .order_by("id_allertamento")
            )
            medieArray.append(mediaTL)

        print("Calcolo media mobile in 12h....")
        data_riferimento = data_emissione + datetime.timedelta(hours=12)
        sommeMedia = []  # type: ignore
        for scadenza in range(9):
            sommeMedia.append([])
            for media in medieArray[scadenza]:
                sommeMedia[scadenza].append(media.numeric_value)

            area = 0
            for media in medieArray[scadenza + 1]:
                sommeMedia[scadenza][area] += media.numeric_value
                area += 1

        timelayouts12h = [48, 1011, 64, 1013, 65, 1015, 81, 1017, 82]

        for scadenza in range(9):
            area = 0
            for media in medieArray[scadenza]:
                newforecastzone = models.ForecastZone(
                    id_allertamento=media.id_allertamento,
                    id_parametro=parametro_dict["PLUV"],
                    id_aggregazione=aggregazione_dict["901"],
                    model_type="DMO",
                    model_name="PSA_00_DO",
                    data_emissione=data_emissione,
                    data_riferimento=data_riferimento,
                    valore_originale=sommeMedia[scadenza][area],
                    valore_validato=None,
                    last_update=inizio,
                    username=request.user.username,
                )
                newforecastzone.save()
                new901 = models.W30Data(
                    id_w30=w30,
                    id_aggregazione=aggregazione_dict["901"],
                    id_allertamento=media.id_allertamento,
                    id_parametro=parametro_dict["PLUV"],
                    id_time_layouts=time_layouts_dict[timelayouts12h[scadenza]],
                    numeric_value=sommeMedia[scadenza][area],
                )
                new901.save()
                area += 1
            data_riferimento = data_riferimento + datetime.timedelta(hours=6)

        timelayouts24h = [2010, 2011, 66, 2014, 2015, 2016, 83]

        print("Calcolo media mobile in 24h....")
        data_riferimento = data_emissione + datetime.timedelta(hours=24)
        sommeMedia = []
        for scadenza in range(7):
            sommeMedia.append([])
            for media in medieArray[scadenza]:
                sommeMedia[scadenza].append(media.numeric_value)

            for offset in range(1, 4):
                area = 0
                for media in medieArray[scadenza + offset]:
                    sommeMedia[scadenza][area] += media.numeric_value
                    area += 1

        for scadenza in range(7):
            area = 0
            for media in medieArray[scadenza]:
                newforecastzone = models.ForecastZone(
                    id_allertamento=media.id_allertamento,
                    id_parametro=parametro_dict["PLUV"],
                    id_aggregazione=aggregazione_dict["902"],
                    model_type="DMO",
                    model_name="PSA_00_DO",
                    data_emissione=data_emissione,
                    data_riferimento=data_riferimento,
                    valore_originale=sommeMedia[scadenza][area],
                    valore_validato=None,
                    last_update=inizio,
                    username=request.user.username,
                )
                newforecastzone.save()

                new902 = models.W30Data(
                    id_w30=w30,
                    id_aggregazione=aggregazione_dict["902"],
                    id_allertamento=media.id_allertamento,
                    id_parametro=parametro_dict["PLUV"],
                    id_time_layouts=time_layouts_dict[timelayouts24h[scadenza]],
                    numeric_value=sommeMedia[scadenza][area],
                )
                new902.save()

                area += 1
            data_riferimento = data_riferimento + datetime.timedelta(hours=6)

        timelayouts48h = [3010, 3011, 3012]

        print("Calcolo media mobile in 48h....")
        data_riferimento = data_emissione + datetime.timedelta(hours=48)
        sommeMedia = []
        for scadenza in range(3):
            sommeMedia.append([])
            for media in medieArray[scadenza]:
                sommeMedia[scadenza].append(media.numeric_value)

            for offset in range(1, 8):
                area = 0
                for media in medieArray[scadenza + offset]:
                    sommeMedia[scadenza][area] += media.numeric_value
                    area += 1

        for scadenza in range(0, 3, 1):
            area = 0
            for media in medieArray[scadenza]:
                newforecastzone = models.ForecastZone(
                    id_allertamento=media.id_allertamento,
                    id_parametro=parametro_dict["PLUV"],
                    id_aggregazione=aggregazione_dict["903"],
                    model_type="DMO",
                    model_name="PSA_00_DO",
                    data_emissione=data_emissione,
                    data_riferimento=data_riferimento,
                    valore_originale=sommeMedia[scadenza][area],
                    valore_validato=None,
                    last_update=inizio,
                    username=request.user.username,
                )
                newforecastzone.save()

                new903 = models.W30Data(
                    id_w30=w30,
                    id_aggregazione=aggregazione_dict["903"],
                    id_allertamento=media.id_allertamento,
                    id_parametro=parametro_dict["PLUV"],
                    id_time_layouts=time_layouts_dict[timelayouts48h[scadenza]],
                    numeric_value=sommeMedia[scadenza][area],
                )
                new903.save()

                area += 1
            data_riferimento = data_riferimento + datetime.timedelta(hours=6)

        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("psa", w30.id_w30)
        return Response({"id_w30": w30.id_w30})


class W30CurrentView(RetrieveAPIView):
    """
    View the latest W30 bulletin sent for a certain day
    """

    queryset = models.W30.objects.filter(status="1").order_by("-last_update")
    serializer_class = W30SerializerFull

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(
            queryset, data_emissione__date=self.kwargs["data_emissione"]
        )
        self.check_object_permissions(self.request, obj)
        return obj


class W30CurrentDataView(ListAPIView):
    """
    View the aggregated bulletin Data for the last 4 bulletins from the supplied date backwards
    """

    queryset = models.W30Data.objects.all()
    serializer_class = W30CurrentDataViewSerializer

    def list(self, request, *args, **kwargs):
        print("list!")
        data_emissione = self.kwargs["data_emissione"]
        print("data_emissione = ", data_emissione)
        queryset = self.get_queryset().raw(
            """
            WITH d AS (
                SELECT
                    w30_data.id_w30_data,
                    w30_data.numeric_value,
                    w30_data.id_aggregazione,
                    w30_data.id_allertamento,
                    w30_data.id_parametro,
                    w30_data.id_time_layouts,
                    w30_data.id_w30,
                    w30.data_emissione::DATE + MAKE_INTERVAL(
                        days => time_layouts.start_day_offset) + time_layouts.start_time AS start,
                    w30.data_emissione::DATE + MAKE_INTERVAL(
                        days => time_layouts.end_day_offset) + time_layouts.end_time AS end,
                    w30.last_update
                FROM
                    w30
                    JOIN w30_data ON w30.id_w30 = w30_data.id_w30
                    JOIN time_layouts ON w30_data.id_time_layouts = time_layouts.id_time_layouts
                WHERE
                    w30.status = '1'
                    AND w30.data_emissione::DATE > ('{}'::DATE - INTERVAL '4 days')::DATE
                    AND w30.data_emissione::DATE <= '{}'::DATE
            ),
            d1 AS (
                SELECT
                    *,
                    rank() OVER (
                        PARTITION BY start, "end", id_aggregazione, id_allertamento, id_parametro
                        ORDER BY last_update DESC
                    )
                FROM d
            )
            SELECT *
            FROM d1
            WHERE rank = 1""".format(
                data_emissione, data_emissione
            )
        )
        print("queryset = ", type(queryset))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class W30DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W30 bulletin Data to be viewed or edited
    """

    queryset = models.W30Data.objects.all()
    serializer_class = W30DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W30Data.objects
        w30Data = get_object_or_404(queryset, pk=pk)
        serializer = W30DataSerializer(w30Data, context={"request": request})
        return Response(serializer.data)

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w30/data/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w30 = next(s["id"] for s in snapshots if s["id_key"] == "id_w30")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w30",
            "id": id_w30,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w30 = models.W30.objects.get(pk=id_w30)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w30":
                print(
                    "id_w30:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w30, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                print(
                    "id_w30_data:",
                    snapshot["id"],
                    "numeric_value",
                    snapshot["new_value"],
                )
                data = models.W30Data.objects.get(pk=snapshot["id"])
                data.numeric_value = snapshot["new_value"]
                data.save()
                updated += 1
        w30.save()
        fine = datetime.datetime.now()
        serializer = W30SerializerFull(w30, context={"request": request})
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


class HtmlView(DetailView):
    template_name = "psa.html"
    http_method_names = ["get"]
    raise_exception = True
    model = models.W30

    def get_context_data(self, **kwargs):
        queryset = models.W30.objects
        w30 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W30SerializerFull(w30)
        psa = serializer.data
        context = {
            "psa": psa,
        }
        return context


class PdfView(HtmlView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="psa.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class PreviNAView(TemplateView):
    template_name = "psa.txt"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W30.objects
        w30 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W30SerializerFull(w30)
        psa = serializer.data
        psa_rearranged = {}  # type: ignore
        for data in psa["w30data_set"]:
            if data["id_allertamento"] not in psa_rearranged:
                psa_rearranged[data["id_allertamento"]] = {}
            if data["id_parametro"] not in psa_rearranged[data["id_allertamento"]]:
                psa_rearranged[data["id_allertamento"]][data["id_parametro"]] = {}
            if (
                data["id_aggregazione"]
                not in psa_rearranged[data["id_allertamento"]][data["id_parametro"]]
            ):
                psa_rearranged[data["id_allertamento"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ] = {}
            if (
                data["id_time_layouts"]
                not in psa_rearranged[data["id_allertamento"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ]
            ):
                psa_rearranged[data["id_allertamento"]][data["id_parametro"]][
                    data["id_aggregazione"]
                ][data["id_time_layouts"]] = {}
            psa_rearranged[data["id_allertamento"]][data["id_parametro"]][
                data["id_aggregazione"]
            ][data["id_time_layouts"]] = data["numeric_value"]
        # metto la quota neve a "----" se il rispettivo valore di pioggia MAX è 0
        for zona in psa_rearranged:
            for parametro in psa_rearranged[zona]:
                if "PLUV" in parametro:
                    if 125 in psa_rearranged[zona][parametro]:
                        for time_layout in psa_rearranged[zona][parametro][125]:
                            if psa_rearranged[zona][parametro][125][time_layout] == 0:
                                psa_rearranged[zona]["SNOW_LEV"][0][time_layout] = ""
        date_d0 = datetime.datetime.strptime(
            psa["data_emissione"][0:10], "%Y-%m-%d"
        ).strftime("%-d-%b")
        date_d1 = (
            datetime.datetime.strptime(psa["data_emissione"][0:10], "%Y-%m-%d")
            + datetime.timedelta(days=1)
        ).strftime("%-d-%b")
        date_d2 = (
            datetime.datetime.strptime(psa["data_emissione"][0:10], "%Y-%m-%d")
            + datetime.timedelta(days=2)
        ).strftime("%-d-%b")
        date_d3 = (
            datetime.datetime.strptime(psa["data_emissione"][0:10], "%Y-%m-%d")
            + datetime.timedelta(days=3)
        ).strftime("%-d-%b")
        context = {
            "date_d0": date_d0,
            "date_d1": date_d1,
            "date_d2": date_d2,
            "date_d3": date_d3,
            "psa": psa_rearranged,
            "data_emissione": datetime.datetime.strptime(
                psa["data_emissione"][0:10], "%Y-%m-%d"
            ).strftime("%d/%m/%Y"),
        }
        return context
