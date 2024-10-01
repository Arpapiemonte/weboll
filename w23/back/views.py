#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
# import copy
import datetime
import os
import tempfile
from subprocess import call

import pytz
import requests
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from w23.back import models
from w23.back.serializers import (
    SoglieNivoAreaPrevSerializer,
    SogliePluvAreaPrevMassimiSerializer,
    SogliePluvAreaPrevMedieSerializer,
    TimeLayoutsSerializer,
    W23DataSerializer,
    W23EffettiterritorioSerializer,
    W23PericoloSerializer,
    W23Pluvossh6Serializer,
    W23Serializer,
    W23SerializerFull,
    W23ZoneSerializer,
)
from w24.back.models import W24
from website.common.tasks import send_with_celery
from website.common.views import (  # ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core.models import TimeLayouts

# import json
# import os
# import tempfile
# from subprocess import call


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


status_first_time = "X"


class W23View(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletins to be viewed or edited
    """

    queryset = models.W23.objects.order_by("-last_update", "-pk")
    serializer_class = W23Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # crea il nuovo bollettino di oggi
        inizio = datetime.datetime.now()
        today = inizio.date()
        old = (
            models.W23.objects.filter(status="1").order_by("-last_update").latest("pk")
        )
        # gestione anno nuovo
        if old.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            last_seq_num_year = today.year
            new_seq = "1" + "/" + str(last_seq_num_year)
        else:
            last_seq_num = (
                models.W23.objects.filter(data_emissione__year=today.year)
                .exclude(status="0")
                .order_by("-last_update")[0]
                .numero_bollettino
            )
            last_seq_num_year = int(last_seq_num.split("/")[1])
            last_seq_num = last_seq_num.split("/")[0]
            print(last_seq_num)
            new_seq_int = int(last_seq_num) + 1
            new_seq = str(new_seq_int) + "/" + str(last_seq_num_year)

        latest_w24 = (
            W24.objects.filter(status="1")
            .filter(data_emissione=today)
            .order_by("-last_update")
        )
        if latest_w24:
            fraserisknat = latest_w24[0].sintesi_meteo
        else:
            fraserisknat = ""

        new = models.W23(
            data_emissione=today,
            numero_bollettino=new_seq,
            situazione_meteo="",
            status=status_first_time,
            last_update=inizio,
            username=request.user,
            fraserisknat=fraserisknat,
            annotazione="Il bollettino è stato emesso a partire dalla versione base.",
            last_update_annotazione=inizio,
        )
        new.save()
        print("created: ", new)
        print("creazione w23_data...")
        bianco = get_object_or_404(models.W23Pericolo, pk="BIANCO")
        verde = get_object_or_404(models.W23Pericolo, pk="VERDE")
        idrogeologico_oggi = verde
        temporali_oggi = verde
        idraulico_oggi = verde
        neve_oggi = verde
        valanghe_oggi = bianco
        idrogeologico_domani = verde
        temporali_domani = verde
        idraulico_domani = verde
        neve_domani = verde
        valanghe_domani = bianco
        scenario_atteso = "-"

        for zona in models.W23Zone.objects.filter(zona_allerta__iregex=r"^[A-M]$"):
            new_data = models.W23Data(
                id_w23=new,
                id_w23_zone=zona,
                idrogeologico_oggi_for=idrogeologico_oggi,
                idraulico_oggi_for=temporali_oggi,
                temporali_oggi_for=idraulico_oggi,
                neve_oggi_for=neve_oggi,
                valanghe_oggi_for=valanghe_oggi,
                idrogeologico_domani_for=idrogeologico_domani,
                idraulico_domani_for=idraulico_domani,
                temporali_domani_for=temporali_domani,
                neve_domani_for=neve_domani,
                valanghe_domani_for=valanghe_domani,
                idrogeologico_oggi=idrogeologico_oggi,
                temporali_oggi=temporali_oggi,
                idraulico_oggi=idraulico_oggi,
                neve_oggi=neve_oggi,
                valanghe_oggi=valanghe_oggi,
                idrogeologico_domani=idrogeologico_domani,
                temporali_domani=temporali_domani,
                idraulico_domani=idraulico_domani,
                neve_domani=neve_domani,
                valanghe_domani=valanghe_domani,
                scenario_atteso=scenario_atteso,
                scenario_atteso_for=scenario_atteso,
                pluvmax12hd0="0",
                pluvmax12hd1="0",
                pluvmax24hd1="0",
                pluvmax6h18g0="0",
                pluvmax6h00g1="0",
                pluvmax6h06g1="0",
                pluvmax6h12g1="0",
                pluvmax6h18g1="0",
                pluvmax6h00g2="0",
                pluvmax6h06g2="0",
                pluvmax6h12g2="0",
                pluvmax6h18g2="0",
                pluvmax6h00g3="0",
                pluvmed6h18g0="0",
                pluvmed6h00g1="0",
                pluvmed6h06g1="0",
                pluvmed6h12g1="0",
                pluvmed6h18g1="0",
                pluvmed6h00g2="0",
                pluvmed6h06g2="0",
                pluvmed6h12g2="0",
                pluvmed6h18g2="0",
                pluvmed6h00g3="0",
                pluvmed12h18g0_oss="0",
                pluvmed12h00g1="0",
                pluvmed12h06g1="0",
                pluvmed12h12g1="0",
                pluvmed12h18g1="0",
                pluvmed12h00g2="0",
                pluvmed12h06g2="0",
                pluvmed12h12g2="0",
                pluvmed12h18g2="0",
                pluvmed12h00g3="0",
                pluvmed24h18g0_oss="0",
                pluvmed24h00g1_oss="0",
                pluvmed24h06g1_oss="0",
                pluvmed24h12g1="0",
                pluvmed24h18g1="0",
                pluvmed24h00g2="0",
                pluvmed24h06g2="0",
                pluvmed24h12g2="0",
                pluvmed24h18g2="0",
                pluvmed24h00g3="0",
                pluvmed48h18g0_oss="0",
                pluvmed48h00g1_oss="0",
                pluvmed48h06g1_oss="0",
                pluvmed48h12g1_oss="0",
                pluvmed48h18g1_oss="0",
                pluvmed48h00g2_oss="0",
                pluvmed48h06g2_oss="0",
                pluvmed48h12g2="0",
                pluvmed48h18g2="0",
                pluvmed48h00g3="0",
                neveqmin="0",
                neveqmax="0",
                neve400_oggi="0",
                neve400_domani="0",
                neve400_totale="0",
                neve700_oggi="0",
                neve700_domani="0",
                neve700_totale="0",
                neve1000_oggi="0",
                neve1000_domani="0",
                neve1000_totale="0",
                neveqd01="0",
                neveqd02="0",
                neveqd11="0",
                neveqd12="0",
                neveqd13="0",
                neveqd14="0",
                temporale_oggi="",
                temporale_domani="",
            )
            new_data.save()

        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w23": new.id_w23})

        print("created: ", new)

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
        queryset = models.W23.objects
        w23 = get_object_or_404(queryset, pk=pk)
        serializer = W23SerializerFull(w23, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W23.objects
        if (
            instance.id_w23_parent
            and queryset.filter(pk=instance.id_w23_parent).exists()
        ):
            w23 = get_object_or_404(queryset, pk=instance.id_w23_parent)
            w23.status = "1"
            if not User.objects.filter(username=w23.username).exists():
                print("perform_destroy non trovo l'utente " + w23.username)
                w23.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w23.save()
        instance.delete()

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w23/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w23 = next(s["id"] for s in snapshots if s["id_key"] == "id_w23")
        last_update = datetime.datetime.now()
        if self.request.data[1]["value_key"] != "annotazione":
            last_update_snapshot = {
                "id_key": "id_w23",
                "id": id_w23,
                "value_key": "last_update",
                "new_value": last_update,
            }
        else:
            last_update_snapshot = {
                "id_key": "id_w23",
                "id": id_w23,
                "value_key": "last_update_annotazione",
                "new_value": last_update,
            }
        snapshots.append(last_update_snapshot)
        w23 = models.W23.objects.get(pk=id_w23)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w23":
                print(
                    "id_w23:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w23, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                print(
                    "id_w23_data:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                if snapshot["new_value"] in [
                    "ROSSO",
                    "ARANCIONE",
                    "GIALLO",
                    "VERDE",
                    "BIANCO",
                ] and (
                    "_oggi" in snapshot["value_key"]
                    or "_domani" in snapshot["value_key"]
                ):
                    new_value = models.W23Pericolo.objects.get(pk=snapshot["new_value"])
                else:
                    new_value = snapshot["new_value"]
                data = models.W23Data.objects.get(pk=snapshot["id"])
                setattr(data, snapshot["value_key"], new_value)
                data.save()
                updated += 1
        w23.save()
        fine = datetime.datetime.now()
        serializer = W23SerializerFull(w23, context={"request": request})
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

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W23.objects.get(pk=pk)
        print("w23 reopen:", old)
        old.status = "2"
        old_id_w23 = old.id_w23
        old.save()
        new_seq = int(old.numero_bollettino.split("/")[0]) + 1
        anno = int(old.numero_bollettino.split("/")[1])
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.numero_bollettino = f"{new_seq}/{anno}"
        new.last_update = now
        new.username = request.user
        new.id_w23_parent = old_id_w23
        new.save()
        old_data = models.W23Data.objects.filter(id_w23=old_id_w23)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w23 = new
            new_data.save()
        return Response({"id_w23": new.id_w23})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w23 = models.W23.objects.get(pk=pk)
        w23.status = "1"
        w23.username = request.user.username
        w23.last_update = inizio
        w23.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("allerta", w23.id_w23)
        return Response({"id_w23": w23.id_w23})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send_auto(self, request, pk):
        w23 = models.W23.objects.get(pk=pk)
        print(
            "send_auto del bollettino ",
            w23.id_w23,
            "del",
            w23.data_emissione,
            "iniziato",
        )
        send_with_celery("allerta", w23.id_w23, True)
        return Response({"id_w23": w23.id_w23})


class W23CurrentView(RetrieveAPIView):
    """
    View the latest W23 bulletin sent for a certain day
    """

    queryset = models.W23.objects.filter(status="1").order_by("-last_update")
    serializer_class = W23SerializerFull
    lookup_field = "data_emissione"


class W23DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Data to be viewed or edited
    """

    queryset = models.W23Data.objects.all()
    serializer_class = W23DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W23Data.objects
        w23Data = get_object_or_404(queryset, pk=pk)
        serializer = W23DataSerializer(w23Data, context={"request": request})
        return Response(serializer.data)


class W23ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Zone to be viewed
    """

    queryset = models.W23Zone.objects.all()
    serializer_class = W23ZoneSerializer
    permission_classes = [ReadOnly]


class W23PericoloView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Pericolo to be viewed
    """

    queryset = models.W23Pericolo.objects.order_by("sort_index")
    serializer_class = W23PericoloSerializer
    permission_classes = [ReadOnly]


class W23EffettiterritorioView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Effetti sul territorio to be viewed
    """

    queryset = models.W23Effettiterritorio.objects.all()
    serializer_class = W23EffettiterritorioSerializer
    permission_classes = [ReadOnly]


class TimeLayoutsView(viewsets.ModelViewSet):
    queryset = TimeLayouts.objects.all()
    serializer_class = TimeLayoutsSerializer
    permission_classes = [ReadOnly]


class SogliePluvAreaPrevMassimiView(viewsets.ModelViewSet):
    queryset = models.SogliePluvAreaPrevMassimi.objects.order_by("idtab_allertamento")
    serializer_class = SogliePluvAreaPrevMassimiSerializer
    permission_classes = [ReadOnly]


class SogliePluvAreaPrevMedieView(viewsets.ModelViewSet):
    queryset = models.SogliePluvAreaPrevMedie.objects.order_by("idtab_allertamento")
    serializer_class = SogliePluvAreaPrevMedieSerializer
    permission_classes = [ReadOnly]


class SoglieNivoAreaPrevView(viewsets.ModelViewSet):
    queryset = models.SoglieNivoAreaPrev.objects.all()
    serializer_class = SoglieNivoAreaPrevSerializer
    permission_classes = [ReadOnly]


class W23PVFilter(filters.FilterSet):
    class Meta:
        model = models.W23Pluvossh6
        fields = ["data", "area"]


class W23Pluvossh6View(viewsets.ModelViewSet):
    queryset = (
        models.W23Pluvossh6.objects.filter(
            ora__in=["00:00:00", "06:00:00", "12:00:00", "18:00:00"]
        )
        .exclude(ora__gte="18:00:00", data=datetime.datetime.today())
        .order_by("area", "data", "ora")
    )
    serializer_class = W23Pluvossh6Serializer
    filterset_class = W23PVFilter
    permission_classes = [ReadOnly]


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


# convert localized datetime to utc and return a string representing the date and time in ISO 8601 format:
def format_datetime(dt):
    dt_utc = dt.astimezone(pytz.utc)
    return dt_utc.isoformat()


class AllertaHtmlView(TemplateView):
    template_name = "allerta.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W23.objects
        w23 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W23SerializerFull(w23)
        allerta = serializer.data
        convert_to_date(allerta, "data_emissione")
        tomorrow = allerta["data_emissione"] + datetime.timedelta(days=1)
        allerta["zone"] = {}
        livelli_oggi = [
            "idrogeologico_oggi",
            "temporali_oggi",
            "idraulico_oggi",
            "neve_oggi",
            "valanghe_oggi",
        ]
        livelli_domani = [
            "idrogeologico_domani",
            "temporali_domani",
            "idraulico_domani",
            "neve_domani",
            "valanghe_domani",
        ]
        colori = {}
        sort_index = {}
        for pericolo in models.W23Pericolo.objects.all():
            colori[pericolo.id_w23_pericolo] = pericolo.colore_html
            sort_index[pericolo.id_w23_pericolo] = pericolo.sort_index

        for data in allerta["w23data_set"]:
            zona_allerta = data["id_w23_zone"]["zona_allerta"]
            data["id_w23_zone"]["offset"] = -39 * (
                data["id_w23_zone"]["id_w23_zone"] - 1
            )
            lam_oggi = 0
            for livello in livelli_oggi:
                data[livello + "_colore"] = colori[data[livello]]
                lam_oggi = max(lam_oggi, sort_index[data[livello]])
            lam_domani = 0
            for livello in livelli_domani:
                data[livello + "_colore"] = colori[data[livello]]
                lam_domani = max(lam_domani, sort_index[data[livello]])
            lam = max(lam_oggi, lam_domani)
            data["lam_oggi"] = models.W23Pericolo.objects.get(sort_index=lam_oggi)
            data["lam_domani"] = models.W23Pericolo.objects.get(sort_index=lam_domani)
            data["lam"] = models.W23Pericolo.objects.get(sort_index=lam)
            if zona_allerta != "VA":
                allerta["zone"][zona_allerta] = data

        context = {
            "allerta": allerta,
            "tomorrow": tomorrow,
        }
        return context


class AllertaPDFView(AllertaHtmlView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="allerta.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class AllertaPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w23/rupar_pdf/%d" % kwargs["pk"])

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


class AllertaPngOrigView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w23/pdf/%d" % kwargs["pk"])

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


class KmlView(TemplateView):
    template_name = "allerta.kml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W23.objects
        w23 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W23SerializerFull(w23)
        allerta = serializer.data
        convert_to_date(allerta, "data_emissione")
        inizio = datetime.datetime.now()
        data_allerta = datetime.datetime.strptime(
            str(allerta["data_emissione"]), "%Y-%m-%d %H:%M:%S"
        ).strftime("%d-%m-%Y")
        today = inizio.date()
        allerta["zone"] = {}
        livelli_oggi = [
            "idrogeologico_oggi",
            "temporali_oggi",
            "idraulico_oggi",
            "neve_oggi",
            "valanghe_oggi",
        ]
        livelli_domani = [
            "idrogeologico_domani",
            "temporali_domani",
            "idraulico_domani",
            "neve_domani",
            "valanghe_domani",
        ]
        colori = {}
        sort_index = {}
        for pericolo in models.W23Pericolo.objects.all():
            colori[pericolo.id_w23_pericolo] = pericolo.colore_html
            sort_index[pericolo.id_w23_pericolo] = pericolo.sort_index

        for data in allerta["w23data_set"]:
            zona_allerta = data["id_w23_zone"]["zona_allerta"]
            data["id_w23_zone"]["offset"] = -39 * (
                data["id_w23_zone"]["id_w23_zone"] - 1
            )
            lam_oggi = 0
            for livello in livelli_oggi:
                data[livello + "_colore"] = colori[data[livello]]
                lam_oggi = max(lam_oggi, sort_index[data[livello]])
            lam_domani = 0
            for livello in livelli_domani:
                data[livello + "_colore"] = colori[data[livello]]
                lam_domani = max(lam_domani, sort_index[data[livello]])
            lam = max(lam_oggi, lam_domani)

            data["lam_oggi"] = models.W23Pericolo.objects.get(sort_index=lam_oggi)
            data["lam_domani"] = models.W23Pericolo.objects.get(sort_index=lam_domani)
            data["lam"] = models.W23Pericolo.objects.get(sort_index=lam)
            if datetime.datetime.strptime(
                str(allerta["data_emissione"]), "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d") != today.strftime("%d-%m-%Y"):
                data["kml"] = models.W23Pericolo.objects.get(sort_index=lam_domani)
            else:
                data["kml"] = models.W23Pericolo.objects.get(sort_index=lam_oggi)
                data_allerta = datetime.datetime.strptime(
                    str(allerta["data_emissione"] + datetime.timedelta(days=1)),
                    "%Y-%m-%d %H:%M:%S",
                ).strftime("%d-%m-%Y")
            if zona_allerta != "VA":
                allerta["zone"][zona_allerta] = data

        context = {
            "allerta": allerta,
            "data_allerta": data_allerta,
        }
        return context


class Kml36hView(TemplateView):
    template_name = "allerta.kml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W23.objects
        w23 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W23SerializerFull(w23)
        allerta = serializer.data
        convert_to_date(allerta, "data_emissione")
        data_allerta = datetime.datetime.strptime(
            str(allerta["data_emissione"]), "%Y-%m-%d %H:%M:%S"
        ).strftime("%d-%m-%Y")
        allerta["zone"] = {}
        livelli_oggi = [
            "idrogeologico_oggi",
            "temporali_oggi",
            "idraulico_oggi",
            "neve_oggi",
            "valanghe_oggi",
        ]
        livelli_domani = [
            "idrogeologico_domani",
            "temporali_domani",
            "idraulico_domani",
            "neve_domani",
            "valanghe_domani",
        ]
        colori = {}
        sort_index = {}
        for pericolo in models.W23Pericolo.objects.all():
            colori[pericolo.id_w23_pericolo] = pericolo.colore_html
            sort_index[pericolo.id_w23_pericolo] = pericolo.sort_index

        for data in allerta["w23data_set"]:
            zona_allerta = data["id_w23_zone"]["zona_allerta"]
            data["id_w23_zone"]["offset"] = -39 * (
                data["id_w23_zone"]["id_w23_zone"] - 1
            )
            lam_oggi = 0
            for livello in livelli_oggi:
                data[livello + "_colore"] = colori[data[livello]]
                lam_oggi = max(lam_oggi, sort_index[data[livello]])
            lam_domani = 0
            for livello in livelli_domani:
                data[livello + "_colore"] = colori[data[livello]]
                lam_domani = max(lam_domani, sort_index[data[livello]])
            lam = max(lam_oggi, lam_domani)

            data["lam"] = models.W23Pericolo.objects.get(sort_index=lam)
            data["kml"] = models.W23Pericolo.objects.get(sort_index=lam)

            if zona_allerta != "VA":
                allerta["zone"][zona_allerta] = data

        context = {
            "allerta": allerta,
            "data_allerta": data_allerta,
        }
        return context


# find maximum value among all parameters
def massimo(parameters):
    p = parameters.copy()
    p.pop("EFFETTI SUL TERRITORIO", "")
    lookup = {"BIANCO": -1, "VERDE": 0, "GIALLO": 1, "ARANCIONE": 2, "ROSSO": 3}
    m = max(p, key=lambda x: lookup[p[x]])
    return p[m]


def rinomina(parameters):
    mapping = {
        "EFFETTI SUL TERRITORIO": "scenario_atteso",
        "IDRAULICO_1224": "idraulico_oggi",
        "IDRAULICO_2436": "idraulico_domani",
        "IDROGEOLOGICO_1224": "idrogeologico_oggi",
        "IDROGEOLOGICO_2436": "idrogeologico_domani",
        "TEMPORALI_1224": "temporali_oggi",
        "TEMPORALI_2436": "temporali_domani",
        "NEVE_1224": "neve_oggi",
        "NEVE_2436": "neve_domani",
        "VALANGHE_1224": "valanghe_oggi",
        "VALANGHE_2436": "valanghe_domani",
    }
    for new_key, old_key in mapping.items():
        parameters[new_key] = parameters.pop(old_key)


# returns parameters filtered for values containing any of hints and with uppercased key
def filtra_valori(parameters, hints):
    valori = {}
    for k, v in parameters.items():
        delimiter = "_"
        if delimiter in k:
            k_split = k.split(delimiter)
            # escludo gli allarmi derivanti dalle previsioni
            if k_split[len(k_split) - 1] != "for":
                if v in hints:
                    valori[k] = v
        else:
            if v in hints:
                valori[k] = v
    return valori
    # return {k: parameters[k] for k, v in parameters.items() if v in hints}


def parametri(zona):
    return filtra_valori(zona, ["BIANCO", "VERDE", "GIALLO", "ARANCIONE", "ROSSO"])


class XmlView(TemplateView):
    template_name = "allerta.xml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W23.objects
        w23 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W23SerializerFull(w23)
        allerta = serializer.data

        for i, zona in enumerate(allerta["w23data_set"]):
            if zona["id_w23_zone"]["nome_zona"][:4] != "Piem":
                del allerta["w23data_set"][i]

        cet = pytz.timezone("CET")
        fmt = "%Y-%m-%dT%H:%M:%S"
        lu = cet.localize(
            datetime.datetime.strptime(allerta["last_update"], fmt)
        )  # fromisoformat is only available in python 3.7+
        lu13 = lu.replace(hour=13, minute=0, second=0, microsecond=0)
        lu37 = lu.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) + datetime.timedelta(days=2)

        allerta["sent"] = format_datetime(lu)
        allerta["onset"] = format_datetime(lu13)
        allerta["expires"] = format_datetime(lu37)
        allerta["msgType"] = "Update"
        for zona in allerta["w23data_set"]:
            zona["onset"] = allerta["onset"]
            zona["expires"] = allerta["expires"]
            p = {
                k: parametri(zona)[k]
                for k in parametri(zona).keys()
                if "_for" != k[-len("_for") :]
            }
            p["scenario_atteso"] = zona["scenario_atteso"].upper()
            rinomina(p)
            zona["parameters"] = p
            # assegno il colore della criticità
            zona["event"] = massimo(p)

            zona["category"] = "Geo"  # ossia >= a giallo
            if zona["event"] == "VERDE":
                zona["responseType"] = "None"
                zona["urgency"] = "Unknown"
                zona["severity"] = "Unknown"
                zona["category"] = "Met"
            elif zona["event"] == "BIANCO":
                zona["responseType"] = "None"
                zona["urgency"] = "Unknown"
                zona["severity"] = "Unknown"
                zona["category"] = "Met"
            else:
                # se una o più icone sono nere o la criticità è più di verde il tag è prepare
                allerta["msgType"] = "Alert"
                zona["responseType"] = "Prepare"
                zona["urgency"] = "Expected"
                # assegno la severità al colore
                if zona["event"] == "GIALLO":
                    zona["severity"] = "Moderate"
                elif zona["event"] == "ARANCIONE":
                    zona["severity"] = "Severe"
                else:
                    zona["severity"] = "Extreme"

        context = {"allerta": allerta}
        return context
