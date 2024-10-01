#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime

# import json
import os
import tempfile
from base64 import b64encode

# from contextlib import closing
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

from w20.back import models
from w20.back.serializers import (
    W20DataSerializer,
    W20PericoloSerializer,
    W20Serializer,
    W20SerializerFull,
    W20ZoneSerializer,
)
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    StandardResultsSetPagination,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W20View(viewsets.ModelViewSet):
    """
    API endpoint that allows W20 bulletins to be viewed or edited
    """

    queryset = models.W20.objects.order_by("-last_update", "-pk")
    serializer_class = W20Serializer
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
        queryset = models.W20.objects
        w20 = get_object_or_404(queryset, pk=pk)
        serializer = W20SerializerFull(w20, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w20 = models.W20.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w20.id_w20,
            "del",
            w20.data_emissione,
            "iniziato",
        )
        w20.status = "1"
        w20.username = request.user.username
        w20.last_update = inizio
        w20.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("traps", w20.id_w20)
        return Response({"id_w20": w20.id_w20})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today

        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)

        # set url
        url = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")

        # today_bulletins = models.W20.objects.filter(data_emissione=today.date()).count()
        # if today_bulletins >= 1:
        #     raise ExistingTodayBulletin()
        create_empty = False
        if (
            not models.W20.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w20 = (
                models.W20.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w20 = (
                models.W20.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w20.id_w20,
            "del",
            old_w20.data_emissione,
            "iniziato",
        )
        # aumento il sequenziale perchè è una nuova emissione
        numero_bollettino = int(old_w20.numero_bollettino.split("/")[0])
        numero_bollettino = numero_bollettino + 1
        # gestione anno nuovo
        if old_w20.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            numero_bollettino = 1

        new = models.W20(
            data_emissione=emissione.date(),
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            numero_bollettino=str(numero_bollettino) + "/" + str(today.year),
            pioggia_infiltrata=requests.get(
                url + "/idro/map/planari/traps.png"
            ).content,
            neve_equivalente=requests.get(
                url + "/idro/map/planari/swe_langhe.png"
            ).content,
        )
        new.save()

        # inizio lettura tabella di gimli e inserimento in memoria
        # zone = models.W20Zone.objects.all()
        zone = models.W20Zone.objects.order_by("-id_w20_zone")

        firstgues = models.TrapsComuni.objects.filter(data=emissione.date())
        # firstgues = models.TrapsComuni.objects.filter(data="2023-05-31").order_by("-gid")

        w20_data_list = []
        # Gestione mancanza dati ne firstguess
        for traps in zone:
            innesco = "A"
            for first in firstgues:
                if first.comune == (traps.comune).replace(" d'", " ").replace(
                    " ", "_"
                ).replace("'", ""):
                    # print("SI COMUNE",i,first.gid,"|",first.comune.upper(),"|",traps.comune.upper(),"|")
                    if first.stato == 2:
                        innesco = "B"
                    elif first.stato == 3:
                        innesco = "E"
            w20_data_list.append(
                models.W20Data(
                    id_w20=new,
                    id_w20_zone=traps.id_w20_zone,
                    provincia=traps.provincia,
                    comune=traps.comune,
                    if_perc=traps.if_perc,
                    prob_innesco=innesco,
                )
            )

        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w20_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )

        models.W20Data.objects.bulk_create(w20_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w20": new.id_w20})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w20/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w20 = snapshots["id_w20"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w20 = models.W20.objects.get(pk=id_w20)
        for snapshot in snapshots:
            setattr(w20, snapshot, snapshots[snapshot])
        w20.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W20SerializerFull(w20, context={"request": request})
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


class W20DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W20 bulletin Data to be viewed or edited
    """

    queryset = models.W20Data.objects.all()
    serializer_class = W20DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W20Data.objects
        w20Data = get_object_or_404(queryset, pk=pk)
        serializer = W20DataSerializer(w20Data, context={"request": request})
        return Response(serializer.data)


class W20ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W20 bulletin Zone to be viewed or edited
    """

    queryset = models.W20Zone.objects.all()
    serializer_class = W20ZoneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W20PericoloView(viewsets.ModelViewSet):
    """
    API endpoint that allows W20 bulletin Pericolo to be viewed or edited
    """

    queryset = models.W20Pericolo.objects.all()
    serializer_class = W20PericoloSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


class TrapsHTMLView(TemplateView):
    template_name = "traps.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W20.objects
        w20 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W20SerializerFull(w20)
        traps = serializer.data
        convert_to_date(traps, "data_emissione")
        if w20.neve_equivalente is not None:
            neve_equivalente = b64encode(w20.neve_equivalente).decode()

        if w20.pioggia_infiltrata is not None:
            pioggia_infiltrata = b64encode(w20.pioggia_infiltrata).decode()

        context = {
            "traps": traps,
            "title": "Bollettino Traps",
            "neve_equivalente": neve_equivalente,
            "pioggia_infiltrata": pioggia_infiltrata,
        }
        return context


class TrapsPDFView(TrapsHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="traps.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class TrapsPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w20/pdf/%d" % kwargs["pk"])

        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(r.content)
            f.flush()
            png_name = "%s.png" % f.name
            command = (
                "convert -verbose -density 145 -crop 1191x1685+3x5 %s -append %s"
                % (
                    f.name,
                    png_name,
                )
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
