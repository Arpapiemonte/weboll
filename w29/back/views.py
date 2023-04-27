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

from w29.back import models
from w29.back.serializers import (
    W29DataSerializer,
    W29PericoloSerializer,
    W29ProbabilitaSerializer,
    W29Serializer,
    W29SerializerFull,
    W29ZoneSerializer,
)
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    StandardResultsSetPagination,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W29View(viewsets.ModelViewSet):
    """
    API endpoint that allows W29 bulletins to be viewed or edited
    """

    queryset = models.W29.objects.order_by("-last_update", "-pk")
    serializer_class = W29Serializer
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
        queryset = models.W29.objects
        w29 = get_object_or_404(queryset, pk=pk)
        serializer = W29SerializerFull(w29, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w29 = models.W29.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w29.id_w29,
            "del",
            w29.data_emissione,
            "iniziato",
        )
        w29.status = "1"
        w29.username = request.user.username
        w29.last_update = inizio
        w29.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("slops", w29.id_w29)
        return Response({"id_w29": w29.id_w29})

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
        # today_bulletins = models.W29.objects.filter(data_emissione=today.date()).count()
        # if today_bulletins >= 1:
        #     raise ExistingTodayBulletin()
        create_empty = False
        if (
            not models.W29.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w29 = (
                models.W29.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w29 = (
                models.W29.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w29.id_w29,
            "del",
            old_w29.data_emissione,
            "iniziato",
        )
        # aumento il sequenziale perchè è una nuova emissione
        numero_bollettino = int(old_w29.numero_bollettino.split("/")[0])
        numero_bollettino = numero_bollettino + 1
        # gestione anno nuovo
        if old_w29.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            numero_bollettino = 1

        if create_empty:
            situazione_evoluzione = ""
            note = "-"
        else:
            situazione_evoluzione = str(old_w29.situazione_evoluzione)
            note = "-"
        ora_simulazione = "n.d."
        ora_osservazione = "n.d."
        data_osservazione = "n.d."
        data_simulazione = "n.d."
        csvfile = None
        # apertura csv file per first guess
        url = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")
        if url == "http://frontend:80":
            url += "/slops/prog.conf"
        else:
            url += "/prog.conf"
        # controllo che il file ci sia
        try:
            with closing(requests.get(url, stream=True)) as r:
                f = (line.decode("utf-8") for line in r.iter_lines())
                csvfile = csv.reader(f, delimiter=delimiter_firstguess)
                for w29_firstguessdata_tmp in csvfile:
                    # controllo che le colonne siano 11
                    if len(w29_firstguessdata_tmp) == 11:
                        if w29_firstguessdata_tmp[1] == today.strftime("%d/%m/%Y"):
                            ora_simulazione = w29_firstguessdata_tmp[
                                8
                            ]  # da prendere esternamente
                            ora_osservazione = w29_firstguessdata_tmp[
                                10
                            ]  # da prendere esternamente
                            data_osservazione = datetime.datetime.strptime(
                                w29_firstguessdata_tmp[9], "%d/%m/%Y"
                            ).strftime(
                                "%Y-%m-%d"
                            )  # da prendere esternamente
                            data_simulazione = datetime.datetime.strptime(
                                w29_firstguessdata_tmp[1], "%d/%m/%Y"
                            ).strftime(
                                "%Y-%m-%d"
                            )  # da prendere esternamente
        except Exception:
            pass
            print("url non esiste non la trovo")
        new = models.W29(
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

        zone = models.W29Zone.objects.all()
        zone_dict = {}
        for v in zone:
            zone_dict[str(v.id_w29_zone)] = v
        # carico la configurazione json per sapere quanti record ci devono essere su w29_data
        with open("config/w29_data.json") as json_file:
            w29_data_config = json.load(json_file)
        # riempo il dizionario con i dati del json di default
        w29_data_new_dict = {}
        for w in w29_data_config:
            w29_data_new_dict[w29_data_config[w]["id_w29_zone"]] = models.W29Data(
                id_w29=new,
                id_w29_zone=zone_dict[str(w29_data_config[w]["id_w29_zone"])],
                livello_criticita_oss=w29_data_config[w]["livello_criticita_oss"],
                probabilita_criticita_oss=w29_data_config[w][
                    "probabilita_criticita_oss"
                ],
                livello_criticita_prev_oggi=w29_data_config[w][
                    "livello_criticita_prev_oggi"
                ],
                probabilita_criticita_prev_oggi=w29_data_config[w][
                    "probabilita_criticita_prev_oggi"
                ],
                livello_criticita_prev_domani=w29_data_config[w][
                    "livello_criticita_prev_domani"
                ],
                probabilita_criticita_prev_domani=w29_data_config[w][
                    "probabilita_criticita_prev_domani"
                ],
            )
        try:
            with closing(requests.get(url, stream=True)) as r:
                f = (line.decode("utf-8") for line in r.iter_lines())
                csvfile = csv.reader(f, delimiter=delimiter_firstguess)
                if csvfile is not None:
                    #  aggiorno il dizionario con i dati del csv se
                    # il csv  aggiornato e se lo trovo altrimenti metto il default
                    if w29_firstguessdata_tmp[1] == today.strftime("%d/%m/%Y"):
                        for w29_firstguessdata_tmp in csvfile:
                            # w29_firstguessdata_tmp = w.split(delimiter_firstguess)
                            w29_data_new_dict[
                                int(w29_firstguessdata_tmp[0])
                            ].livello_criticita_oss = w29_firstguessdata_tmp[2]
                            w29_data_new_dict[
                                int(w29_firstguessdata_tmp[0])
                            ].probabilita_criticita_oss = w29_firstguessdata_tmp[3]
                            w29_data_new_dict[
                                int(w29_firstguessdata_tmp[0])
                            ].livello_criticita_prev_oggi = w29_firstguessdata_tmp[4]
                            w29_data_new_dict[
                                int(w29_firstguessdata_tmp[0])
                            ].probabilita_criticita_prev_oggi = w29_firstguessdata_tmp[
                                5
                            ]
                            w29_data_new_dict[
                                int(w29_firstguessdata_tmp[0])
                            ].livello_criticita_prev_domani = w29_firstguessdata_tmp[6]
                            w29_data_new_dict[
                                int(w29_firstguessdata_tmp[0])
                            ].probabilita_criticita_prev_domani = w29_firstguessdata_tmp[
                                7
                            ]
        except Exception:
            pass
            print("url non esiste non la trovo")
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w29_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w29_data_list = []
        for w in w29_data_new_dict:
            w29_data_list.append(w29_data_new_dict[w])
        models.W29Data.objects.bulk_create(w29_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w29": new.id_w29})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w29/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w29 = snapshots["id_w29"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w29 = models.W29.objects.get(pk=id_w29)
        for snapshot in snapshots:
            setattr(w29, snapshot, snapshots[snapshot])
        w29.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W29SerializerFull(w29, context={"request": request})
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


class W29DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W29 bulletin Data to be viewed or edited
    """

    queryset = models.W29Data.objects.all()
    serializer_class = W29DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W29Data.objects
        w29Data = get_object_or_404(queryset, pk=pk)
        serializer = W29DataSerializer(w29Data, context={"request": request})
        return Response(serializer.data)


class W29ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W29 bulletin Zone to be viewed or edited
    """

    queryset = models.W29Zone.objects.all()
    serializer_class = W29ZoneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W29PericoloView(viewsets.ModelViewSet):
    """
    API endpoint that allows W29 bulletin Pericolo to be viewed or edited
    """

    queryset = models.W29Pericolo.objects.all()
    serializer_class = W29PericoloSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W29ProbabilitaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W29 bulletin Probabilita to be viewed or edited
    """

    queryset = models.W29Probabilita.objects.all()
    serializer_class = W29ProbabilitaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


class SlopsHTMLView(TemplateView):
    template_name = "slops.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W29.objects
        w29 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W29SerializerFull(w29)
        slops = serializer.data
        convert_to_date(slops, "data_validita")
        convert_to_date(slops, "data_emissione")
        # del slops["w29data_set"]

        context = {"slops": slops, "title": "Bollettino Slops"}
        return context


class SlopsPDFView(SlopsHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="slops.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class SlopsPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w29/pdf/%d" % kwargs["pk"])

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
