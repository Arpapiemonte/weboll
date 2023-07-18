#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime

# import json
# import os
# import tempfile
# from contextlib import closing
# from subprocess import call
# import requests
from django.contrib.auth.models import User
from django.db.transaction import atomic

# from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w26.back import models
from w26.back.serializers import (
    BisBollettinoWebolimpiaSerializer,
    W26DataSerializer,
    W26Serializer,
    W26SerializerFull,
    W26ZoneSerializer,
)
from website.common.tasks import send_with_celery
from website.common.views import (  # ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class DateValiditaFilter(filters.FilterSet):
    data_min = filters.DateFilter(field_name="data_validita", lookup_expr="gte")
    data_max = filters.DateFilter(field_name="data_validita", lookup_expr="lte")

    class Meta:
        model = models.W26
        fields = ["id_w26"]


class W26View(viewsets.ModelViewSet):
    """
    API endpoint that allows W26 bulletins to be viewed or edited
    """

    queryset = models.W26.objects.order_by("-last_update", "-pk")
    serializer_class = W26Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination
    filterset_class = DateValiditaFilter

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
        queryset = models.W26.objects
        w26 = get_object_or_404(queryset, pk=pk)
        serializer = W26SerializerFull(w26, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w26 = models.W26.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w26.id_w26,
            "del",
            w26.data_emissione,
            "iniziato",
        )
        w26.status = "1"
        w26.username = request.user.username
        w26.last_update = inizio
        w26.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("bis", w26.id_w26)
        return Response({"id_w26": w26.id_w26})

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W26.objects
        if (
            instance.id_w26_parent
            and queryset.filter(pk=instance.id_w26_parent).exists()
        ):
            w26 = get_object_or_404(queryset, pk=instance.id_w26_parent)
            w26.status = "1"
            if not User.objects.filter(username=w26.username).exists():
                print("perform_destroy non trovo l'utente " + w26.username)
                w26.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w26.save()
        instance.delete()

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path="new/(?P<validita>[0-9]+(-[0-9]+)+(-[0-9]+)+)",
    )
    @atomic
    def new(self, request, validita):
        print("new,validita-----------", validita)
        # @action(detail=False, permission_classes=[permissions.IsAuthenticated])
        # @atomic
        # def new(self, request):
        # delimiter_firstguess = ";"
        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today

        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)
        # validita = "2023-01-13"

        create_empty = False
        if (
            not models.W26.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w26 = (
                models.W26.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w26 = (
                models.W26.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w26.id_w26,
            "del",
            old_w26.data_emissione,
            "iniziato",
        )
        # aumento il sequenziale perchè è una nuova emissione
        numero_bollettino = int(old_w26.numero_bollettino.split("/")[0])
        numero_bollettino = numero_bollettino + 1
        # gestione anno nuovo
        if old_w26.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            numero_bollettino = 1

        new = models.W26(
            data_emissione=emissione.date(),
            data_validita=validita,
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            numero_bollettino=str(numero_bollettino) + "/" + str(today.year),
        )
        new.save()

        # inizio lettura tabella di gimli e inserimento in memoria
        biss = models.BisBollettinoWebolimpia.objects.filter(data=validita).order_by(
            "numero"
        )
        # print('biss-----------------',bool(biss))
        w26_data_list = []
        # Gestione mancanza dati ne firstguess
        if bool(biss):
            for bis in biss:
                w26_zona = models.W26Zone.objects.get(codice=bis.codice)
                id_nota = ""
                if bis.id_note:
                    id_nota = "(" + str(bis.id_note) + ")"
                w26_data_list.append(
                    models.W26Data(
                        id_w26=new,
                        id_w26_zone=w26_zona,
                        hmin="{:.2f}".format(bis.h_min if bis.h_min is not None else 0),
                        hmax="{:.2f}".format(bis.h_max if bis.h_max is not None else 0),
                        hmed="{:.2f}".format(bis.h_med if bis.h_med is not None else 0),
                        qmin="{:.1f}".format(bis.q_min if bis.q_min is not None else 0),
                        qmax="{:.1f}".format(bis.q_max if bis.q_max is not None else 0),
                        qmed="{:.1f}".format(bis.q_med if bis.q_med is not None else 0),
                        nota=bis.note,
                        idnota=id_nota,
                    )
                )
        else:
            w26_data_list.append(
                models.W26Data(
                    id_w26=new,
                    id_w26_zone=models.W26Zone.objects.get(id_w26_zone="1"),
                    hmin="ND",
                    hmax="ND",
                    hmed="ND",
                    qmin="ND",
                    qmax="ND",
                    qmed="ND",
                    nota="ND",
                    idnota="ND",
                )
            )
        models.W26Data.objects.bulk_create(w26_data_list)

        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w26": new.id_w26})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W26.objects.get(pk=pk)
        print("w26 reopen:", old)
        old.status = "2"
        old_id_w26 = old.id_w26
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w26_parent = old_id_w26
        new.save()
        # print('created: ', new)
        old_data = models.W26Data.objects.filter(id_w26=old_id_w26)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w26 = new
            new_data.save()

        return Response({"id_w26": new.id_w26})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w26/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w26 = snapshots["id_w26"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w26 = models.W26.objects.get(pk=id_w26)
        for snapshot in snapshots:
            setattr(w26, snapshot, snapshots[snapshot])
        w26.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W26SerializerFull(w26, context={"request": request})
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


class W26DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W26 bulletin Data to be viewed or edited
    """

    queryset = models.W26Data.objects.all()
    serializer_class = W26DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W26Data.objects
        w26Data = get_object_or_404(queryset, pk=pk)
        serializer = W26DataSerializer(w26Data, context={"request": request})
        return Response(serializer.data)


class W26SVGView(TemplateView):
    template_name = "bis.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W26.objects
        w26 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W26SerializerFull(w26)
        w26_json = serializer.data
        w26_json["data_emissione"] = w26.data_emissione
        w26_json["last_update"] = w26.last_update
        w26_json["w26data_set"].sort(key=lambda x: x["id_w26_zone"]["numero"])
        context = {"w26": w26_json, "title": "Bollettino BIS"}
        return context


class W26PDFView(W26SVGView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="w26.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class DataFilter(filters.FilterSet):
    data_min = filters.DateFilter(field_name="data", lookup_expr="gte")
    data_max = filters.DateFilter(field_name="data", lookup_expr="lte")

    class Meta:
        model = models.BisBollettinoWebolimpia
        fields = ["codice"]


class BisBollettinoWebolimpiaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W26 bulletins to be viewed or edited
    """

    queryset = models.BisBollettinoWebolimpia.objects.order_by("-data")
    serializer_class = BisBollettinoWebolimpiaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    filterset_class = DataFilter


class W26ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W26 bulletin Zone to be viewed or edited
    """

    queryset = models.W26Zone.objects.all()
    serializer_class = W26ZoneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
