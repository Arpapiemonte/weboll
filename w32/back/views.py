#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
import csv
import datetime
import json
import os
import tempfile
from contextlib import closing
from subprocess import call

import requests

# from django.contrib.auth.models import User
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

from w32.back import models
from w32.back.serializers import (
    W32DataSerializer,
    W32MbaciniDataSerializer,
    W32MbaciniSerializer,
    W32PericolombaciniSerializer,
    W32PericoloSerializer,
    W32Serializer,
    W32SerializerFull,
    W32ZoneSerializer,
)
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    StandardResultsSetPagination,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W32View(viewsets.ModelViewSet):
    """
    API endpoint that allows W32 bulletins to be viewed or edited
    """

    queryset = models.W32.objects.order_by("-last_update", "-pk")
    serializer_class = W32Serializer
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
        queryset = models.W32.objects
        w32 = get_object_or_404(queryset, pk=pk)
        serializer = W32SerializerFull(w32, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w32 = models.W32.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w32.id_w32,
            "del",
            w32.data_emissione,
            "iniziato",
        )
        w32.status = "1"
        w32.username = request.user.username
        w32.last_update = inizio
        w32.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("defense", w32.id_w32)
        return Response({"id_w32": w32.id_w32})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        delimiter_firstguess = ";"
        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today
        minuti_emissione = inizio.minute
        h_emissione = inizio.hour
        if minuti_emissione > 0:
            ora_emissione = str(h_emissione + 1) + ":00"

        else:
            ora_emissione = str(h_emissione) + ":00"

        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = emissione + datetime.timedelta(days=1)
        # today_bulletins = models.W32.objects.filter(data_emissione=today.date()).count()
        # if today_bulletins >= 1:
        #     raise ExistingTodayBulletin()
        create_empty = False
        if (
            not models.W32.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w32 = (
                models.W32.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w32 = (
                models.W32.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w32.id_w32,
            "del",
            old_w32.data_emissione,
            "iniziato",
        )
        # aumento il sequenziale perchè è una nuova emissione
        numero_bollettino = int(old_w32.numero_bollettino.split("/")[0])
        numero_bollettino = numero_bollettino + 1
        # gestione anno nuovo
        if old_w32.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            numero_bollettino = 1

        if create_empty:
            situazione_evoluzione = ""
            note = "-"
        else:
            situazione_evoluzione = str(old_w32.situazione_evoluzione)
            note = "-"
        ora_simulazione = "n.d."
        ora_osservazione = "n.d."
        data_osservazione = "n.d."
        data_simulazione = "n.d."
        csvfile = None
        # apertura csv file per first guess
        # apertura csv file per first guess
        url = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")
        if url == "http://frontend:80":
            url += "/defense/defense_qpe.conf"
        else:
            url += "/defense_qpe.conf"
        print("url......", url)
        # url = "http://perseo.ad.arpa.piemonte.it/defense_qpe.conf"
        urlmbacini = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")
        if urlmbacini == "http://frontend:80":
            urlmbacini += "/defense/defense_qpe_macrobacini.conf"
        else:
            urlmbacini += "/defense_qpe_macrobacini.conf"
        print("urlmbacini......", urlmbacini)
        # urlmbacini = "http://perseo.ad.arpa.piemonte.it/defense_qpe_macrobacini.conf"
        # controllo che il file ci sia
        try:
            with closing(requests.get(url, stream=True)) as r:
                f = (line.decode("utf-8") for line in r.iter_lines())
                csvfile = csv.reader(f, delimiter=delimiter_firstguess)
                for w32_firstguessdata_tmp in csvfile:
                    # controllo che le colonne siano 8
                    if len(w32_firstguessdata_tmp) == 8:
                        if w32_firstguessdata_tmp[4] == today.strftime("%Y-%m-%d"):
                            ora_simulazione = w32_firstguessdata_tmp[
                                7
                            ]  # da prendere esternamente
                            ora_osservazione = w32_firstguessdata_tmp[
                                5
                            ]  # da prendere esternamente
                            data_osservazione = datetime.datetime.strptime(
                                w32_firstguessdata_tmp[4], "%Y-%m-%d"
                            ).strftime(
                                "%Y-%m-%d"
                            )  # da prendere esternamente
                            data_simulazione = datetime.datetime.strptime(
                                w32_firstguessdata_tmp[6], "%Y-%m-%d"
                            ).strftime(
                                "%Y-%m-%d"
                            )  # da prendere esternamente
        except Exception:
            pass
            print("url non esiste non la trovo")
        new = models.W32(
            data_emissione=emissione.date(),
            data_validita=tomorrow.date(),
            situazione_evoluzione=situazione_evoluzione,
            note=note,
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            ora_simulazione=ora_simulazione,  # da prendere esternamente
            ora_osservazione=ora_osservazione,  # da prendere esternamente
            data_osservazione=data_osservazione,  # da prendere esternamente
            data_simulazione=data_simulazione,  # da prendere esternamente
            ora_emissione=ora_emissione,
            numero_bollettino=str(numero_bollettino) + "/" + str(today.year),
        )
        new.save()

        zone = models.W32Zone.objects.all()
        zone_dict = {}
        for v in zone:
            zone_dict[str(v.id_w32_zone)] = v
        # carico la configurazione json per sapere quanti record ci devono essere su w32_data
        with open("config/w32_data.json") as json_file:
            w32_data_config = json.load(json_file)
        # riempo il dizionario con i dati del json di default
        w32_data_new_dict = {}
        for w in w32_data_config:
            w32_data_new_dict[w32_data_config[w]["id_w32_zone"]] = models.W32Data(
                id_w32=new,
                id_w32_zone=zone_dict[str(w32_data_config[w]["id_w32_zone"])],
                livello_criticita_oss=w32_data_config[w]["livello_criticita_oss"],
                livello_criticita_prev_oggi=w32_data_config[w][
                    "livello_criticita_prev_oggi"
                ],
                livello_criticita_prev_domani=w32_data_config[w][
                    "livello_criticita_prev_domani"
                ],
            )
        try:
            with closing(requests.get(url, stream=True)) as r:
                f = (line.decode("utf-8") for line in r.iter_lines())
                csvfile = csv.reader(f, delimiter=delimiter_firstguess)
                if csvfile is not None:
                    #  aggiorno il dizionario con i dati del csv se
                    # il csv  aggiornato e se lo trovo altrimenti metto il default
                    numriga = 1
                    if w32_firstguessdata_tmp[4] == today.strftime("%Y-%m-%d"):
                        # if w32_firstguessdata_tmp[1] == today.strftime("%d/%m/%Y"):
                        for w32_firstguessdata_tmp in csvfile:
                            # print('w32_firstguessdata_tmp---------',w32_firstguessdata_tmp)
                            # w32_firstguessdata_tmp = w.split(delimiter_firstguess)
                            w32_data_new_dict[
                                numriga
                            ].livello_criticita_oss = w32_firstguessdata_tmp[1]
                            w32_data_new_dict[
                                numriga
                            ].livello_criticita_prev_oggi = w32_firstguessdata_tmp[2]
                            w32_data_new_dict[
                                numriga
                            ].livello_criticita_prev_domani = w32_firstguessdata_tmp[3]
                            numriga = numriga + 1
        except Exception:
            pass
            print("url non esiste non la trovo")
        mbacini = models.W32Mbacini.objects.all()
        mbacini_dict = {}
        for v in mbacini:
            mbacini_dict[str(v.id_w32_mbacini)] = v
        # carico la configurazione json per sapere quanti record ci devono essere su w32_data
        with open("config/w32_mbacini_data.json") as json_file:
            w32_mbacini_data_config = json.load(json_file)
        # print('w32_mbacini_data_config========',w32_mbacini_data_config)
        # riempo il dizionario con i dati del json di default
        w32_mbacini_data_new_dict = {}
        for w in w32_mbacini_data_config:
            w32_mbacini_data_new_dict[
                w32_mbacini_data_config[w]["id_w32_mbacini"]
            ] = models.W32MbaciniData(
                id_w32=new,
                id_w32_mbacini=mbacini_dict[
                    str(w32_mbacini_data_config[w]["id_w32_mbacini"])
                ],
                livello_criticita_oss=w32_mbacini_data_config[w][
                    "livello_criticita_oss"
                ],
                livello_criticita_prev_oggi=w32_mbacini_data_config[w][
                    "livello_criticita_prev_oggi"
                ],
                livello_criticita_prev_domani=w32_mbacini_data_config[w][
                    "livello_criticita_prev_domani"
                ],
            )
        try:
            with closing(requests.get(urlmbacini, stream=True)) as r:
                f = (line.decode("utf-8") for line in r.iter_lines())
                csvfile = csv.reader(f, delimiter=delimiter_firstguess)
                for w32_firstguessmbacinidata_tmp in csvfile:
                    if len(w32_firstguessmbacinidata_tmp) == 9:
                        if csvfile is not None:
                            numrigam = 1
                            with closing(requests.get(urlmbacini, stream=True)) as r1:
                                f1 = (line.decode("utf-8") for line in r1.iter_lines())
                                csvfile = csv.reader(f1, delimiter=delimiter_firstguess)
                                if w32_firstguessmbacinidata_tmp[6] == today.strftime(
                                    "%Y-%m-%d"
                                ):
                                    for w32_firstguessmbacinidata_tmp in csvfile:
                                        w32_mbacini_data_new_dict[
                                            numrigam
                                        ].livello_criticita_oss = w32_firstguessmbacinidata_tmp[
                                            1
                                        ]
                                        w32_mbacini_data_new_dict[
                                            numrigam
                                        ].livello_criticita_prev_oggi = w32_firstguessmbacinidata_tmp[
                                            2
                                        ]
                                        w32_mbacini_data_new_dict[
                                            numrigam
                                        ].livello_criticita_prev_domani = w32_firstguessmbacinidata_tmp[
                                            3
                                        ]
                                        numrigam = numrigam + 1
        except Exception:
            pass
            print("urlmbacini non esiste non la trovo")
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w32_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w32_data_list = []
        for w in w32_data_new_dict:
            w32_data_list.append(w32_data_new_dict[w])
        models.W32Data.objects.bulk_create(w32_data_list)
        w32_mbacini_data_list = []
        for w in w32_mbacini_data_new_dict:
            w32_mbacini_data_list.append(w32_mbacini_data_new_dict[w])
        models.W32MbaciniData.objects.bulk_create(w32_mbacini_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w32": new.id_w32})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w32/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w32 = snapshots["id_w32"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w32 = models.W32.objects.get(pk=id_w32)
        for snapshot in snapshots:
            setattr(w32, snapshot, snapshots[snapshot])
        w32.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W32SerializerFull(w32, context={"request": request})
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


class W32DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W32 bulletin Data to be viewed or edited
    """

    queryset = models.W32Data.objects.all()
    serializer_class = W32DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W32Data.objects
        w32Data = get_object_or_404(queryset, pk=pk)
        serializer = W32DataSerializer(w32Data, context={"request": request})
        return Response(serializer.data)


class W32MbaciniDataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W32 bulletin MbaciniData to be viewed or edited
    """

    queryset = models.W32MbaciniData.objects.all()
    serializer_class = W32MbaciniDataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W32MbaciniData.objects
        w32Data = get_object_or_404(queryset, pk=pk)
        serializer = W32MbaciniDataSerializer(w32Data, context={"request": request})
        return Response(serializer.data)


class W32ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W32 bulletin Zone to be viewed or edited
    """

    queryset = models.W32Zone.objects.all()
    serializer_class = W32ZoneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W32PericoloView(viewsets.ModelViewSet):
    """
    API endpoint that allows W32 bulletin Pericolo to be viewed or edited
    """

    queryset = models.W32Pericolo.objects.all()
    serializer_class = W32PericoloSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W32PericolombaciniView(viewsets.ModelViewSet):
    """
    API endpoint that allows W32 bulletin Pericolombacini to be viewed or edited
    """

    queryset = models.W32Pericolombacini.objects.all()
    serializer_class = W32PericolombaciniSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W32MbaciniView(viewsets.ModelViewSet):
    """
    API endpoint that allows W32 bulletin Probabilita to be viewed or edited
    """

    queryset = models.W32Mbacini.objects.all()
    serializer_class = W32MbaciniSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


def calcolomaxmbacini(defense):
    vd = {}
    for area in defense["w32mbacinidata_set"]:
        if (
            area["livello_criticita_oss"] == "S"
            or area["livello_criticita_prev_oggi"] == "S"
            or area["livello_criticita_prev_domani"] == "S"
        ):
            vd[area["id_w32_mbacini"]["id_w32_mbacini"]] = "S"
        elif (
            area["livello_criticita_oss"] == "np"
            and area["livello_criticita_prev_oggi"] == "np"
            and area["livello_criticita_prev_domani"] == "np"
        ):
            vd[area["id_w32_mbacini"]["id_w32_mbacini"]] = "np"
        else:
            vd[area["id_w32_mbacini"]["id_w32_mbacini"]] = "-"
    maxdefense = vd
    return maxdefense


class DefenseHTMLView(TemplateView):
    template_name = "defense.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W32.objects
        w32 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W32SerializerFull(w32)
        defense = serializer.data
        maxdefense = calcolomaxmbacini(defense)
        convert_to_date(defense, "data_validita")
        convert_to_date(defense, "data_emissione")
        # del defense["w32data_set"]

        context = {
            "defense": defense,
            "title": "Bollettino Defense",
            "maxdefense": maxdefense,
        }
        return context


class DefensePDFView(DefenseHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="defense.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class DefensePngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w32/pdf/%d" % kwargs["pk"])

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
