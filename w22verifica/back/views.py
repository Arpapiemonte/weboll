#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
import csv
import datetime
import json

# import os
# import tempfile
from contextlib import closing
from os import getenv

import requests

# from django.contrib.auth.models import User
from django.db.transaction import atomic

# from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w22verifica.back import models
from w22verifica.back.serializers import (
    W22GiudizioSerializer,
    W22SeveritaSerializer,
    W22VerificaDataSerializer,
    W22VerificaSerializer,
    W22VerificaSerializerFull,
    W22ZoneSerializer,
)
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    StandardResultsSetPagination,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W22VerificaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletins to be viewed or edited
    """

    queryset = models.W22Verifica.objects.order_by("-last_update", "-pk")
    serializer_class = W22VerificaSerializer
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
        queryset = models.W22Verifica.objects
        w22verifica = get_object_or_404(queryset, pk=pk)
        serializer = W22VerificaSerializerFull(
            w22verifica, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w22verifica = models.W22Verifica.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w22verifica.id_w22verifica,
            "del",
            w22verifica.data_emissione,
            "iniziato",
        )
        w22verifica.status = "1"
        w22verifica.username = request.user.username
        w22verifica.last_update = inizio
        w22verifica.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("verificapiene", w22verifica.id_w22verifica)
        return Response({"id_w22verifica": w22verifica.id_w22verifica})

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path="new/(?P<num_bollettino>[0-9]+(_[0-9]+)+)",
    )
    @atomic
    def new(self, request, num_bollettino):
        print("new,num_bollettino-----------", num_bollettino)
        delimiter_firstguess = ";"
        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)

        create_empty = False
        if (
            not models.W22Verifica.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w22verifica = (
                models.W22Verifica.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w22verifica = (
                models.W22Verifica.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w22verifica.id_w22verifica,
            "del",
            old_w22verifica.data_emissione,
            "iniziato",
        )
        # gestione anno nuovo
        if old_w22verifica.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            # numero_bollettino = 1

        if create_empty:
            situazione_evoluzione = "-Note:"
            note = "Nulla da segnalare oggi"
        else:
            situazione_evoluzione = str(old_w22verifica.situazione_evoluzione)
            note = "-"
        data_analisi_csv = str(today)[:10]
        data_emissione_csv = str(today)[:10]
        giudizio = "1"
        id_numero_bollettino = "0_0"
        numero_bollettino = "0/0"
        csvfile = None
        # apertura csv file per first guess
        url = (
            getenv("BASE_DATA_URL_FULL", "http://frontend:80")
            + "/piene_valutazione_bollettino/piene_valutazione_bollettino_"
            + num_bollettino
            + ".csv"
        )
        num_bollettinotemp = num_bollettino.split("_")
        numero_bollettino = num_bollettinotemp[0] + "/" + num_bollettinotemp[1]
        print(url)
        # controllo che il file ci sia
        try:
            with closing(requests.get(url, stream=True)) as r:
                f = (line.decode("utf-8") for line in r.iter_lines())
                csvfile = csv.reader(f, delimiter=delimiter_firstguess)
                for w22verifica_firstguessdata_tmp in csvfile:
                    # print(w22verifica_firstguessdata_tmp[1].split(" ")[0])
                    # controllo che le colonne del csv siano 9
                    if len(w22verifica_firstguessdata_tmp) == 9:
                        data_analisi_csv = w22verifica_firstguessdata_tmp[2].split(" ")[
                            0
                        ]  # da prendere esternamente
                        data_emissione_csv = w22verifica_firstguessdata_tmp[1].split(
                            " "
                        )[
                            0
                        ]  # da prendere esternamente
                        giudizio = w22verifica_firstguessdata_tmp[
                            7
                        ]  # da prendere esternamente
                        id_numero_bollettino = num_bollettino
                        # numero_bollettino = num_bollettino
                        numero_bollettino = numero_bollettino
        except Exception:
            pass
            print("url non esiste non la trovo", url)
        print("url esiste", url)
        new = models.W22Verifica(
            data_emissione=data_emissione_csv,
            data_analisi=data_analisi_csv,
            situazione_evoluzione=situazione_evoluzione,
            annotazione=note,
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            id_numero_bollettino=id_numero_bollettino,
            numero_bollettino=numero_bollettino,
            id_w22giudizio=giudizio,  # da prendere esternamente
        )
        new.save()
        zone = models.W22Zone.objects.all()
        zone_dict = {}
        for v in zone:
            zone_dict[str(v.id_w22_zone)] = v
        # carico la configurazione json per sapere quanti record ci devono essere su w29_data
        with open("config/w22verifica_data.json") as json_file:
            w22verifica_data_config = json.load(json_file)
        # riempo il dizionario con i dati del json di default
        w22verifica_data_new_dict = {}
        for w in w22verifica_data_config:
            w22verifica_data_new_dict[w22verifica_data_config[w]["id_w22_zone"]] = (
                models.W22VerificaData(
                    id_w22verifica=new,
                    id_w22_zone=zone_dict[
                        str(w22verifica_data_config[w]["id_w22_zone"])
                    ],
                    prev_crit_tot=w22verifica_data_config[w]["prev_crit_tot"],
                    oss_crit_tot=w22verifica_data_config[w]["oss_crit_tot"],
                    err_crit_tot=w22verifica_data_config[w]["err_crit_tot"],
                )
            )
        try:
            with closing(requests.get(url, stream=True)) as r:
                f = (line.decode("utf-8") for line in r.iter_lines())
                csvfile = csv.reader(f, delimiter=delimiter_firstguess)
                if csvfile is not None:
                    for w22verifica_firstguessdata_tmp in csvfile:
                        # w22verifica_firstguessdata_tmp = w.split(
                        #     delimiter_firstguess
                        # )
                        w22verifica_data_new_dict[
                            int(w22verifica_firstguessdata_tmp[3])
                        ].prev_crit_tot = w22verifica_firstguessdata_tmp[4]
                        w22verifica_data_new_dict[
                            int(w22verifica_firstguessdata_tmp[3])
                        ].oss_crit_tot = w22verifica_firstguessdata_tmp[5]
                        w22verifica_data_new_dict[
                            int(w22verifica_firstguessdata_tmp[3])
                        ].err_crit_tot = w22verifica_firstguessdata_tmp[6]
        except Exception:
            pass
            print("url non esiste non la trovo data")
        print("url esiste data")
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w22verifica_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w22verifica_data_list = []
        for w in w22verifica_data_new_dict:
            w22verifica_data_list.append(w22verifica_data_new_dict[w])
        models.W22VerificaData.objects.bulk_create(w22verifica_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w22verifica": new.id_w22verifica})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w22verifica/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w22verifica = snapshots["id_w22verifica"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w22verifica = models.W22Verifica.objects.get(pk=id_w22verifica)
        for snapshot in snapshots:
            setattr(w22verifica, snapshot, snapshots[snapshot])
        w22verifica.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W22VerificaSerializerFull(
            w22verifica, context={"request": request}
        )
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


class W22GiudizioView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Tendenza to be viewed
    """

    queryset = models.W22Giudizio.objects.order_by("id_w22giudizio")
    serializer_class = W22GiudizioSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W22SeveritaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Criticità to be viewed
    """

    queryset = models.W22Severita.objects.order_by("id_w22severita")
    serializer_class = W22SeveritaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W22VerificaDataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Data to be viewed or edited
    """

    queryset = models.W22VerificaData.objects.all()
    serializer_class = W22VerificaDataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W22VerificaData.objects
        w22verificaData = get_object_or_404(queryset, pk=pk)
        serializer = W22VerificaDataSerializer(
            w22verificaData, context={"request": request}
        )

        return Response(serializer.data)


class W22ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Zone to be viewed or edited
    """

    queryset = models.W22Zone.objects.all()
    serializer_class = W22ZoneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class VerificaPieneHTMLView(TemplateView):
    template_name = "verificapiene.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W22Verifica.objects
        w22verifica = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W22VerificaSerializerFull(w22verifica)
        verificapiene = serializer.data

        context = {"verificapiene": verificapiene, "title": "Bollettino verifica piene"}
        return context


class VerificaPienePDFView(VerificaPieneHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="verificapiene.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response
