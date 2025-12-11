#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
import math

# import locale
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

from w37.back import models
from w37.back.serializers import W37DataSerializer, W37Serializer, W37SerializerFull
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W37View(viewsets.ModelViewSet):
    """
    API endpoint that allows W37 bulletins to be viewed or edited
    """

    queryset = models.W37.objects.order_by("-last_update", "-pk")
    serializer_class = W37Serializer
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

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W37.objects
        if (
            instance.id_w37_parent
            and queryset.filter(pk=instance.id_w37_parent).exists()
        ):
            w37 = get_object_or_404(queryset, pk=instance.id_w37_parent)
            w37.status = "1"
            if not User.objects.filter(username=w37.username).exists():
                print("perform_destroy non trovo l'utente " + w37.username)
                w37.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w37.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W37.objects
        w37 = get_object_or_404(queryset, pk=pk)
        serializer = W37SerializerFull(w37, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w37 = models.W37.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w37.id_w37,
            "del",
            w37.data_emissione,
            "iniziato",
        )
        w37.status = "1"
        w37.username = request.user.username
        w37.last_update = inizio
        w37.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("aggiornamento_allerta", w37.id_w37)
        return Response({"id_w37": w37.id_w37})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # delimiter_firstguess = ";"
        delimiter = "__"

        def HashW37Data(codice_comune, id_parametro, id_time_layouts):
            return (
                str(codice_comune)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_time_layouts)
            )

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

        # set url
        url = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")

        # tomorrow = emissione + datetime.timedelta(days=1)
        # today_bulletins = models.W37.objects.filter(data_emissione=today.date()).count()
        # if today_bulletins >= 1:
        #     raise ExistingTodayBulletin()
        old_w37 = None
        if (
            models.W37.objects.filter(status="1")
            .filter(data_emissione__day=today.day)
            .order_by("-last_update")
            .exists()
        ):
            old_w37 = (
                models.W37.objects.filter(status="1")
                .filter(data_emissione__day=today.day)
                .order_by("-last_update")
                .latest("pk")
            )
        if old_w37 is not None:
            print(
                "new del bollettino ",
                old_w37.id_w37,
                "del",
                old_w37.data_emissione,
                "iniziato",
            )
            # aumento il sequenziale perchè è una nuova emissione
            numero_bollettino = int(old_w37.numero_bollettino)  # type: ignore
            numero_bollettino = numero_bollettino + 1
        else:
            numero_bollettino = 1

        # if create_empty:
        situazione_attuale = "-"
        previsione_meteo = "-"
        previsione_idro = "-"
        # else:
        #     annotazione = str(old_w22.annotazione)
        #     situazione_evoluzione = str(old_w22.situazione_evoluzione)

        # print("old_w37", old_w37)
        url_img_03_h = url + "/sc05_intranet/public/cf/pericolo/stato_piemonte_03h.png"
        url_img_24_h = url + "/sc05_intranet/public/cf/pericolo/stato_piemonte_24h.png"
        print("leggo l'immagine: " + url_img_03_h)
        print("leggo l'immagine: " + url_img_24_h)
        new = models.W37(
            data_emissione=emissione.date(),
            ora_emissione=ora_emissione,
            data_aggiornamento=None,  # type: ignore
            ora_aggiornamento=None,
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            numero_bollettino=str(numero_bollettino),
            mappa_24h=requests.get(url_img_24_h).content,
            mappa_3h=requests.get(url_img_03_h).content,
            situazione_attuale=situazione_attuale,
            previsione_meteo=previsione_meteo,
            previsione_idro=previsione_idro,
        )
        new.save()

        # riempo il dizionario con i dati del json del pericolo
        w37_data_list = []
        url2 = url + "/sc05_intranet/public/cf/pericolo/pericolo_piemonte.json"
        print("leggo il json: " + url2)
        pericoloh24_config = json.loads(requests.get(url2).content)
        url2 = url + "/sc05_intranet/public/cf/pericolo/web_pericolo.json"
        print("leggo il json: " + url2)
        pericolo_config = json.loads(requests.get(url2).content)
        for feature in pericolo_config:
            for feature2 in pericoloh24_config["features"]:
                if feature["comune"] == feature2["properties"]["comune"]:
                    w37_data_record = models.W37Data(
                        id_w37=new,
                        comune=feature["comune"],
                        area=feature["area"],
                        sigla_prov=feature["sigla_pro"],
                        pericolo=feature2["properties"]["stato"],
                        pluvio=feature["pluv"],
                        idro=feature["idro"],
                        temporali=feature["storm"],
                    )
            if (
                w37_data_record.idro != 0
                or w37_data_record.pluvio != 0
                or w37_data_record.temporali != 0
                or w37_data_record.pericolo != 0
            ):
                if w37_data_record.pluvio != -99:
                    if w37_data_record.pluvio != -1:
                        w37_data_list.append(w37_data_record)
            # w37_data_list.append(w37_data_record)
        # FINE dati del json del pericolo

        # w37_data_new_dict = {}  # type: ignore

        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w37_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )

        models.W37Data.objects.bulk_create(w37_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w37": new.id_w37})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W37.objects.get(pk=pk)
        # print("w37 reopen:", old)
        old.status = "2"
        old_id_w37 = old.id_w37
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w37_parent = old_id_w37
        new.save()
        # print('created: ', new)
        old_data = models.W37Data.objects.filter(id_w37=old_id_w37)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w37 = new
            new_data.save()

        return Response({"id_w37": new.id_w37})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reload_data(self, request, pk):
        # set url
        url = os.getenv("BASE_DATA_URL_FULL", "http://frontend:80")
        # riapre un bollettino
        now = datetime.datetime.now()
        w37 = models.W37.objects.get(pk=pk)
        # print("w37 reopen:", old)
        url_img_03_h = url + "/sc05_intranet/public/cf/pericolo/stato_piemonte_03h.png"
        url_img_24_h = url + "/sc05_intranet/public/cf/pericolo/stato_piemonte_24h.png"
        print("rileggo l'immagine: " + url_img_03_h)
        print("rileggo l'immagine: " + url_img_24_h)
        w37.mappa_24h = requests.get(url_img_24_h).content
        w37.mappa_3h = requests.get(url_img_03_h).content
        w37.last_update = now
        w37.save()
        models.W37Data.objects.filter(id_w37=w37.id_w37).delete()
        # riempo il dizionario con i dati del json del pericolo
        w37_data_list = []
        url2 = url + "/sc05_intranet/public/cf/pericolo/pericolo_piemonte.json"
        print("rileggo il json: " + url2)
        pericoloh24_config = json.loads(requests.get(url2).content)
        url2 = url + "/sc05_intranet/public/cf/pericolo/web_pericolo.json"
        print("rileggo il json: " + url2)
        pericolo_config = json.loads(requests.get(url2).content)
        for feature in pericolo_config:
            for feature2 in pericoloh24_config["features"]:
                if feature["comune"] == feature2["properties"]["comune"]:
                    w37_data_record = models.W37Data(
                        id_w37=w37,
                        comune=feature["comune"],
                        area=feature["area"],
                        sigla_prov=feature["sigla_pro"],
                        pericolo=feature2["properties"]["stato"],
                        pluvio=feature["pluv"],
                        idro=feature["idro"],
                        temporali=feature["storm"],
                    )
            if (
                w37_data_record.idro != 0
                or w37_data_record.pluvio != 0
                or w37_data_record.temporali != 0
                or w37_data_record.pericolo != 0
            ):
                if w37_data_record.pluvio != -99:
                    if w37_data_record.pluvio != -1:
                        w37_data_list.append(w37_data_record)

        models.W37Data.objects.bulk_create(w37_data_list)

        return Response({"id_w37": w37.id_w37})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w37/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w37 = snapshots["id_w37"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w37 = models.W37.objects.get(pk=id_w37)
        for snapshot in snapshots:
            setattr(w37, snapshot, snapshots[snapshot])
        w37.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W37SerializerFull(w37, context={"request": request})
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


class W37DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W37 bulletin Data to be viewed or edited
    """

    queryset = models.W37Data.objects.all()
    serializer_class = W37DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W37Data.objects
        w37Data = get_object_or_404(queryset, pk=pk)
        serializer = W37DataSerializer(w37Data, context={"request": request})
        return Response(serializer.data)


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%dT%H:%M:%S",
    )


class AggiornamentoHTMLView(TemplateView):
    template_name = "aggiornamento.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W37.objects
        w37 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W37SerializerFull(w37)
        aggiornamento = serializer.data
        mapping = {
            -1: 99,
            -99: 99,
            0: 0,
            1: -1,
            2: -2,
            3: -3,
        }

        aggiornamento["w37data_set"].sort(
            key=lambda x: (
                mapping.get(x["pericolo"], 0),
                mapping.get(x["idro"], 0),
                mapping.get(x["pluvio"], 0),
                x["comune"],
            )
        )

        convert_to_date(aggiornamento, "data_emissione")
        if len(aggiornamento["w37data_set"]) != 0:
            pagecounter = math.ceil(len(aggiornamento["w37data_set"]) / 35)
        else:
            pagecounter = 0
        # print("pagecounter", pagecounter)

        context = {
            "aggiornamento": aggiornamento,
            "pagecounter": range(pagecounter),
        }
        return context


class AggiornamentoPDFView(AggiornamentoHTMLView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="aggiornamento.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class AggiornamentoPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        django_url = os.getenv("DJANGO_URL", "http://django:8000")
        r = requests.get(django_url + "/w37/pdf/%d" % kwargs["pk"])

        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(r.content)
            f.flush()
            png_name = "%s.png" % f.name
            command = "convert -verbose -density 145 -crop 1191x1685+3x5 %s -append %s" % (
                # command = "convert -verbose -density 145 -crop 1191x1685+3x5 %s %s" % (
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
