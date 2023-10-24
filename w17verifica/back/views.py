#
# Copyright (C) 2020-2023 simevo s.r.l. for ARPA Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

import datetime
import json

# from django.contrib.auth.models import User
# from django.db.models import Q
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from w17.back.models import W17
from w17verifica.back import models
from w17verifica.back.serializers import (
    W17verificaDataSerializer,
    W17verificaMassimaliSerializer,
    W17verificaSerializer,
    W17verificaSerializerFull,
)
from website.common.tasks import send_with_celery

# from website.common.views import BulletinDraftLocked, StandardResultsSetPagination
from website.common.views import StandardResultsSetPagination

# from website.core.models import WeatherValues
from website.core.models import W05


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W17verificaDataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W17verifica bulletin Data to be viewed or edited
    """

    queryset = models.w17_verifica_data.objects.all()
    serializer_class = W17verificaDataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.w17_verifica_data.objects
        w17verificaData = get_object_or_404(queryset, pk=pk)
        serializer = W17verificaDataSerializer(
            w17verificaData, context={"request": request}
        )
        return Response(serializer.data)


class W17verificaMassimaliSerializerView(viewsets.ModelViewSet):
    """
    API endpoint that allows W17verificaMassimali bulletin Data to be viewed or edited
    """

    queryset = models.w17_verifica_massimali.objects.all()
    serializer_class = W17verificaMassimaliSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.w17_verifica_massimali.objects
        w17verificaMassimali = get_object_or_404(queryset, pk=pk)
        serializer = W17verificaMassimaliSerializer(
            w17verificaMassimali, context={"request": request}
        )
        return Response(serializer.data)


class W17verificaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W31 bulletins to be viewed or edited
    """

    queryset = models.w17_verifica.objects.order_by("-last_update", "-pk")
    serializer_class = W17verificaSerializer
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
        queryset = models.w17_verifica.objects
        w17_verifica = get_object_or_404(queryset, pk=pk)
        serializer = W17verificaSerializerFull(
            w17_verifica, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # crea il nuovo bollettino di oggi

        now = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today.replace(hour=12, minute=30, second=0, microsecond=0)
        emissionew05 = today.replace(hour=14, minute=0, second=0, microsecond=0)
        next_blt_time = today + datetime.timedelta(days=1)
        tomorrow = emissione + datetime.timedelta(days=-1)

        def day_forecast(i):
            # print("day_forecast", i)
            forecast = emissione + datetime.timedelta(days=-(1 + i))
            # print("forecast", forecast)
            # "2023-06-03"
            data_forecast = datetime.datetime.strptime(
                str(forecast), "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d")
            return data_forecast

        # cerca il bollettino di analisi di oggi
        bollettinoanalisi = (
            W17.objects.filter(data_emissione=day_forecast(-1))
            .filter(status="1")
            .count()
        )
        # Creo il bollettino solo se presente analisi di oggi
        if bollettinoanalisi > 0:
            print("bullettinoanalisi-----------", bollettinoanalisi)
            new = models.w17_verifica(
                data_emissione=emissione,
                next_blt_time=next_blt_time,
                data_analysis=tomorrow,
                status="X",
                last_update=now,
                username=request.user,
            )
            new.save()
            # INIZIO
            # carico la configurazione json per sapere quanti record ci devono essere su w29_data
            with open("config/w17verifica_data.json") as json_file:
                w17verifica_data_config = json.load(json_file)
            # riempo il dizionario con i dati del json di default
            w17verifica_data_new_dict = {}
            # for w in w17verifica_data_config:
            bullettin0 = (
                W05.objects.filter(
                    start_valid_time=emissionew05 - datetime.timedelta(days=1)
                )
                .filter(status="1")
                .get()
            )
            w17verifica_data_new_dict[
                w17verifica_data_config["0"]["id_w17_verifica_data"]
            ] = models.w17_verifica_data(
                id_w17verifica=new,
                id_w05=bullettin0,  # da cercare nel meteo di riferimeto
                data_forecast=day_forecast(
                    w17verifica_data_config["0"]["id_w17_verifica_data"]
                ),
                # id_w17_verifica_data=zone_dict[str(w17verifica_data_config[0]["id_w17_verifica_data"])],
                coerenza_mattino_nubi=w17verifica_data_config["0"][
                    "coerenza_mattino_nubi"
                ],
                coerenza_mattino_pioggia=w17verifica_data_config["0"][
                    "coerenza_mattino_pioggia"
                ],
                coerenza_pomeriggio_nubi=w17verifica_data_config["0"][
                    "coerenza_pomeriggio_nubi"
                ],
                coerenza_pomeriggio_pioggia=w17verifica_data_config["0"][
                    "coerenza_pomeriggio_pioggia"
                ],
                forecast_id=w17verifica_data_config["0"]["forecast_id"],
                # id_w17_verifica_data=w17verifica_data_config["0"]["id_w17_verifica_data"],
                punteggio_nubi=w17verifica_data_config["0"]["punteggio_nubi"],
                punteggio_pioggia=w17verifica_data_config["0"]["punteggio_pioggia"],
                punteggio_relativo=w17verifica_data_config["0"]["punteggio_relativo"],
                punteggio_temperatura=w17verifica_data_config["0"][
                    "punteggio_temperatura"
                ],
                punteggio_vento=w17verifica_data_config["0"]["punteggio_vento"],
                punteggio_zero_quota_neve=w17verifica_data_config["0"][
                    "punteggio_zero_quota_neve"
                ],
            )
            bullettin1 = (
                W05.objects.filter(
                    start_valid_time=emissionew05 - datetime.timedelta(days=2)
                )
                .filter(status="1")
                .get()
            )
            # record 1
            w17verifica_data_new_dict[
                w17verifica_data_config["1"]["id_w17_verifica_data"]
            ] = models.w17_verifica_data(
                id_w17verifica=new,
                id_w05=bullettin1,  # da cercare nel meteo di riferimeto
                data_forecast=day_forecast(
                    w17verifica_data_config["1"]["id_w17_verifica_data"]
                ),
                # id_w17_verifica_data=zone_dict[str(w17verifica_data_config["1"]["id_w17_verifica_data"])],
                coerenza_mattino_nubi=w17verifica_data_config["1"][
                    "coerenza_mattino_nubi"
                ],
                coerenza_mattino_pioggia=w17verifica_data_config["1"][
                    "coerenza_mattino_pioggia"
                ],
                coerenza_pomeriggio_nubi=w17verifica_data_config["1"][
                    "coerenza_pomeriggio_nubi"
                ],
                coerenza_pomeriggio_pioggia=w17verifica_data_config["1"][
                    "coerenza_pomeriggio_pioggia"
                ],
                forecast_id=w17verifica_data_config["1"]["forecast_id"],
                # id_w17_verifica_data=w17verifica_data_config["1"]["id_w17_verifica_data"],
                punteggio_nubi=w17verifica_data_config["1"]["punteggio_nubi"],
                punteggio_pioggia=w17verifica_data_config["1"]["punteggio_pioggia"],
                punteggio_relativo=w17verifica_data_config["1"]["punteggio_relativo"],
                punteggio_temperatura=w17verifica_data_config["1"][
                    "punteggio_temperatura"
                ],
                punteggio_vento=w17verifica_data_config["1"]["punteggio_vento"],
                punteggio_zero_quota_neve=w17verifica_data_config["1"][
                    "punteggio_zero_quota_neve"
                ],
            )
            bullettin2 = (
                W05.objects.filter(
                    start_valid_time=emissionew05 - datetime.timedelta(days=3)
                )
                .filter(status="1")
                .get()
            )
            # record 2
            w17verifica_data_new_dict[
                w17verifica_data_config["2"]["id_w17_verifica_data"]
            ] = models.w17_verifica_data(
                id_w17verifica=new,
                id_w05=bullettin2,  # da cercare nel meteo di riferimeto
                data_forecast=day_forecast(
                    w17verifica_data_config["2"]["id_w17_verifica_data"]
                ),
                # id_w17_verifica_data=zone_dict[str(w17verifica_data_config["2"]["id_w17_verifica_data"])],
                coerenza_mattino_nubi=w17verifica_data_config["2"][
                    "coerenza_mattino_nubi"
                ],
                coerenza_mattino_pioggia=w17verifica_data_config["2"][
                    "coerenza_mattino_pioggia"
                ],
                coerenza_pomeriggio_nubi=w17verifica_data_config["2"][
                    "coerenza_pomeriggio_nubi"
                ],
                coerenza_pomeriggio_pioggia=w17verifica_data_config["2"][
                    "coerenza_pomeriggio_pioggia"
                ],
                forecast_id=w17verifica_data_config["2"]["forecast_id"],
                # id_w17_verifica_data=w17verifica_data_config["2"]["id_w17_verifica_data"],
                punteggio_nubi=w17verifica_data_config["2"]["punteggio_nubi"],
                punteggio_pioggia=w17verifica_data_config["2"]["punteggio_pioggia"],
                punteggio_relativo=w17verifica_data_config["2"]["punteggio_relativo"],
                punteggio_temperatura=w17verifica_data_config["2"][
                    "punteggio_temperatura"
                ],
                punteggio_vento=w17verifica_data_config["2"]["punteggio_vento"],
                punteggio_zero_quota_neve=w17verifica_data_config["2"][
                    "punteggio_zero_quota_neve"
                ],
            )
            fine = datetime.datetime.now()
            print(
                "inizio salvataggioin w17verifica_data ",
                abs((fine - now).total_seconds()),
                "secondi",
            )
            w17verifica_data_list = []
            for w in w17verifica_data_new_dict:
                w17verifica_data_list.append(w17verifica_data_new_dict[w])
            models.w17_verifica_data.objects.bulk_create(w17verifica_data_list)

            fine = datetime.datetime.now()
            print(
                "new finito in ",
                abs((fine - now).total_seconds()),
                "secondi",
            )
            return Response({"id_w17verifica": new.id_w17verifica})
        else:
            str_error = "Non trovo l'analisi del " + day_forecast(-1)
            print(str_error)
            return Response(data={"error": str_error}, status=555)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # TBD
        return Response({"id_w17verifica": 1})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def copy(self, request, pk):
        # TBD
        return Response({"id_w17verifica": 1})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w17verifica = models.w17_verifica.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w17verifica.id_w17verifica,
            "del",
            w17verifica.data_emissione,
            "iniziato",
        )
        w17verifica.status = "1"
        w17verifica.username = request.user.username
        w17verifica.last_update = inizio
        w17verifica.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("w17verifica", w17verifica.id_w17verifica)
        return Response({"id_w17verifica": w17verifica.id_w17verifica})
        # return Response({"id_w17verifica": 1})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w17verifica/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w17verifica = snapshots["id_w17verifica"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w17verifica = models.w17_verifica.objects.get(pk=id_w17verifica)
        for snapshot in snapshots:
            setattr(w17verifica, snapshot, snapshots[snapshot])
        w17verifica.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W17verificaSerializerFull(
            w17verifica, context={"request": request}
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


class HtmlView(TemplateView):
    template_name = "w17verifica.html"
    http_method_names = ["get"]
    raise_exception = True
    model = models.w17_verifica

    def get_context_data(self, **kwargs):
        queryset = models.w17_verifica.objects
        w17verifca = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W17verificaSerializerFull(w17verifca)
        w17verifca_data = serializer.data
        context = {
            "w17verifca_data": w17verifca_data,
        }
        return context


class PdfView(HtmlView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="w17verifica.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response
