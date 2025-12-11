#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import datetime
import os

from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from w16.back.serializers import (
    OzonoLivelliSerializer,
    W16ConfSerializer,
    W16DataSerializer,
    W16Serializer,
    W16SerializerFull,
)
from website.common.tasks import send_with_celery
from website.common.views import BulletinDraftLocked, StandardResultsSetPagination
from website.core import models

levels = [
    {"id_ozono_livelli": 1, "soglia_inferiore_mxd": 0, "soglia_inferiore_mx8": 0},
    {"id_ozono_livelli": 2, "soglia_inferiore_mxd": 180, "soglia_inferiore_mx8": 110},
    {"id_ozono_livelli": 3, "soglia_inferiore_mxd": 240, "soglia_inferiore_mx8": 140},
    {"id_ozono_livelli": 4, "soglia_inferiore_mxd": 360, "soglia_inferiore_mx8": 220},
]


def livello_proposto_mx8(value):
    return max(0, sum([value > x["soglia_inferiore_mx8"] for x in levels]) - 1)


def livello_proposto_mxd(value):
    return max(0, sum([value > x["soglia_inferiore_mxd"] for x in levels]) - 1)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W16View(viewsets.ModelViewSet):
    """
    API endpoint that allows W16 bulletins to be viewed or edited
    """

    queryset = models.W16.objects.order_by("-last_update", "-seq_num", "-pk")
    serializer_class = W16Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        month = self.request.query_params.get("month", "all")
        year = self.request.query_params.get("year", "all")
        order = self.request.query_params.get("order", "-last_update")

        if month != "all":
            queryset = (
                self.get_queryset()
                .filter(start_valid_time__year=year)
                .filter(start_valid_time__month=month)
                .order_by(order)
            )
        elif year != "all":
            queryset = self.filter_queryset(
                self.get_queryset().filter(start_valid_time__year=year).order_by(order)
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
        queryset = models.W16.objects
        if (
            instance.id_w16_parent
            and queryset.filter(pk=instance.id_w16_parent).exists()
        ):
            w16 = get_object_or_404(queryset, pk=instance.id_w16_parent)
            w16.status = "1"
            if not User.objects.filter(username=w16.username).exists():
                print("perform_destroy non trovo l'utente " + w16.username)
                w16.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w16.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W16.objects
        w16 = get_object_or_404(queryset, pk=pk)
        serializer = W16SerializerFull(w16, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # crea il nuovo bollettino di oggi
        print("w016 new")
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        emissione = today.replace(hour=12, minute=30, second=0, microsecond=0)
        next_blt_time = emissione + datetime.timedelta(days=1)
        old = (
            models.W16.objects.filter(status="1").order_by("-last_update").latest("pk")
        )
        # gestione anno nuovo
        if old.start_valid_time.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            new_seq = 1
        else:
            last_seq_num = (
                models.W16.objects.filter(start_valid_time__year=today.year)
                .exclude(status="0")
                .latest("seq_num")
                .seq_num
            )
            new_seq = last_seq_num + 1  # type: ignore
        old_id_w16 = old.id_w16
        new = models.W16(
            start_valid_time=emissione,  # devono essere le 12:30
            validity=72,
            next_blt_time=next_blt_time,
            made_by="1",  # 0 = Automatic; 1 = Manual
            note="NULLA DA SEGNALARE",
            status=0,  # il nuovo bollettino lo metto in bozza
            last_update=now,
            username=request.user,
            seq_num=new_seq,  # incremento il sequenziale
            version=0,
            id_w16_parent=None,
        )
        new.save()
        print("created: ", new)
        old_data = models.W16Data.objects.filter(id_w16=old_id_w16)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.data_emissione = today
            new_data.data_scadenza = today + datetime.timedelta(
                days=new_data.id_scadenza - 1
            )
            new_data.id_w16 = new
            new_data.save()
            print(
                "========== created w16_data: ",
                new_data.pk,
                "id_scadenza:",
                new_data.id_scadenza,
            )
            qa_misure = models.QaMisure.objects.filter(
                data_emissione=today,
                id_venue=new_data.id_ozono_zone.pk,
                id_scadenza=new_data.id_scadenza,
            )
            mx8_90p = 0
            mxd_90p = 0
            for misura in qa_misure:
                if misura.id_qa_aggregazione == 1:
                    mx8_90p = misura.valore_validato_num  # type: ignore
                if misura.id_qa_aggregazione == 6:
                    mxd_90p = misura.valore_validato_num  # type: ignore
                new_data1 = models.W16Data1(
                    id_w16_data=new_data,
                    id_qa_parametro=misura.id_qa_parametro,
                    id_ozono_aggregazione=models.OzonoAggregazione.objects.get(
                        pk=misura.id_qa_aggregazione
                    ),
                    valore_num=misura.valore_validato_num,
                    id_strumentazione=misura.id_strumentazione,
                )
                new_data1.save()
                print("created w16_data1: ", new_data1.pk)
            if mx8_90p + mxd_90p > 0:
                livello_proposto = (
                    max(livello_proposto_mx8(mx8_90p), livello_proposto_mxd(mxd_90p))
                    + 1
                )
                new_data.id_ozono_livelli = models.OzonoLivelli.objects.get(
                    pk=livello_proposto
                )
                new_data.save()
        return Response({"id_w16": new.id_w16})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W16.objects.get(pk=pk)
        print("w016 reopen:", old)
        old.status = 2
        old_id_w16 = old.id_w16
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = 0
        new.version = 0
        new.last_update = now
        new.username = request.user
        new.id_w16_parent = old_id_w16
        new.made_by = "1"  # 0 = Automatic; 1 = Manual
        new.save()
        # print('created: ', new)
        old_data = models.W16Data.objects.filter(id_w16=old_id_w16)
        for data in old_data:
            data_id_w16_data = data.id_w16_data
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w16 = new
            new_data.save()
            # print('created: ', new_data)
            old_data1 = models.W16Data1.objects.filter(id_w16_data=data_id_w16_data)
            for data1 in old_data1:
                new_data1 = data1
                new_data1.pk = None
                new_data1.id_w16_data = new_data
                new_data1.save()
                # print('created: ', new_data1)
        return Response({"id_w16": new.id_w16})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def copy(self, request, pk):
        # copia un bollettino
        print("w016 copy:", pk)
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        emissione = today.replace(hour=12, minute=30, second=0, microsecond=0)
        next_blt_time = emissione + datetime.timedelta(days=1)
        old = models.W16.objects.get(pk=pk)
        old_id_w16 = old.id_w16
        # TODO: gestire il cambio dell'anno
        last_seq_num = (
            models.W16.objects.filter(start_valid_time__year=today.year)
            .exclude(status="0")
            .latest("seq_num")
            .seq_num
        )
        new_seq = last_seq_num + 1  # type: ignore
        new = models.W16(
            start_valid_time=emissione,  # devono essere le 12:30
            validity=72,
            next_blt_time=next_blt_time,
            made_by="1",  # 0 = Automatic; 1 = Manual
            note="NULLA DA SEGNALARE",
            status=0,  # il nuovo bollettino lo metto in bozza
            last_update=now,
            username=request.user,
            seq_num=new_seq,  # incremento il sequenziale
            version=0,
            id_w16_parent=None,
        )
        new.save()
        print("created: ", new)

        delta_days = (today.date() - old.start_valid_time.date()).days
        print(
            "difference in days between reference bulletin and new bulletin: ",
            delta_days,
        )

        old_data = models.W16Data.objects.filter(id_w16=old_id_w16).order_by(
            "-id_scadenza"
        )
        for data in old_data:
            data_id_w16_data = data.id_w16_data
            data_id_scadenza = data.id_scadenza
            print("looking at", data_id_scadenza)
            if data_id_scadenza - delta_days >= 0:
                new_data = data
                # resetta la chiave primaria rendendolo un nuovo record
                new_data.pk = None
                new_data.id_w16 = new
                new_data.id_scadenza = data_id_scadenza - delta_days
                print("shifted to", data_id_scadenza - delta_days)
                new_data.data_emissione = today
                new_data.data_scadenza = next_blt_time
                new_data.data_scadenza = today + datetime.timedelta(
                    days=new_data.id_scadenza - 1
                )
                new_data.save()
                print("shifted: ", new_data)
                old_data1 = models.W16Data1.objects.filter(id_w16_data=data_id_w16_data)
                for data1 in old_data1:
                    new_data1 = data1
                    new_data1.pk = None
                    new_data1.id_w16_data = new_data
                    new_data1.save()
                    print("shifted: ", new_data1)
            else:
                print("created new record for", 4 + data_id_scadenza - delta_days)
                new_data = models.W16Data(
                    id_w16=new,
                    id_ozono_zone=data.id_ozono_zone,
                    data_emissione=emissione,
                    data_scadenza=next_blt_time,
                    id_scadenza=4 + data_id_scadenza - delta_days,
                    id_ozono_livelli=models.OzonoLivelli.objects.get(pk=0),
                )
                new_data.save()
                print("shifted: ", new_data)

        return Response({"id_w16": new.id_w16})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w16 = models.W16.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w16.id_w16,
            "del",
            w16.start_valid_time,
            "iniziato",
        )
        w16.status = "1"
        w16.username = request.user.username
        w16.last_update = inizio
        w16.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("ozono", w16.id_w16)
        return Response({"id_w16": w16.id_w16})


class OzonoLivelliView(viewsets.ModelViewSet):
    """
    API endpoint that allows OzonoLivelli records to be viewed
    """

    queryset = models.OzonoLivelli.objects.filter(
        valid_to__date__gt=datetime.datetime.today()
    ).filter(id_ozono_livelli__gt=0)
    serializer_class = OzonoLivelliSerializer
    permission_classes = [ReadOnly]


class W16ConfView(viewsets.ModelViewSet):
    """
    API endpoint that allows W16Conf records to be viewed
    """

    queryset = models.W16Conf.objects.all()
    serializer_class = W16ConfSerializer
    permission_classes = [ReadOnly]


class W16DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W16 bulletin Data to be viewed or updated
    """

    queryset = models.W16Data.objects.all()
    serializer_class = W16DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w16/data/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w16 = next(s["id"] for s in snapshots if s["id_key"] == "id_w16")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w16",
            "id": id_w16,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w16 = models.W16.objects.get(pk=id_w16)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w16":
                print(
                    "id_w16:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w16, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                print(
                    "id_w16_data:",
                    snapshot["id"],
                    "id_ozono_livelli",
                    snapshot["new_value"],
                )
                data = models.W16Data.objects.get(pk=snapshot["id"])
                data.id_ozono_livelli = models.OzonoLivelli.objects.get(
                    pk=snapshot["new_value"]
                )
                data.save()
                updated += 1
        w16.save()
        fine = datetime.datetime.now()
        serializer = W16SerializerFull(w16, context={"request": request})
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


def convert_to_datetime(d, k):
    d[k] = datetime.datetime.strptime(
        d[k].split(".")[0],
        "%Y-%m-%dT%H:%M:%S",
    )


class OzonoSVGView(TemplateView):
    template_name = "ozono.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W16.objects
        w16 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W16SerializerFull(w16)
        ozono = serializer.data
        ozono["logo"] = "ozono_logo"
        convert_to_datetime(ozono, "next_blt_time")
        convert_to_datetime(ozono, "start_valid_time")
        for data in ozono["w16data_set"]:
            convert_to_datetime(data, "data_emissione")
        yesterday = ozono["w16data_set"][0]["data_emissione"] - datetime.timedelta(
            days=1
        )
        today = ozono["w16data_set"][0]["data_emissione"]
        tomorrow = ozono["w16data_set"][0]["data_emissione"] + datetime.timedelta(
            days=1
        )
        tdat = ozono["w16data_set"][0]["data_emissione"] + datetime.timedelta(days=2)
        context = {
            "ozono": ozono,
            "title": "Bollettino Ozono",
            "dates": [
                yesterday,
                today,
                tomorrow,
                tdat,
            ],
        }
        return context


class OzonoPDFView(OzonoSVGView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="ozono.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response
