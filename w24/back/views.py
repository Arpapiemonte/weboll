#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt

import datetime
import os
import tempfile
from decimal import Decimal
from subprocess import call

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

from w24.back import models
from w24.back.serializers import (
    ForecastZoneSerializer,
    W24DataSerializer,
    W24Serializer,
    W24SerializerFull,
    W24SoglieSerializer,
)
from w30.back.models import W30, W30Data
from website.common.tasks import send_with_celery
from website.common.views import BulletinDraftLocked, StandardResultsSetPagination


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W24View(viewsets.ModelViewSet):
    """
    API endpoint that allows W24 bulletins to be viewed or edited
    """

    queryset = models.W24.objects.order_by("-last_update", "-pk")
    serializer_class = W24Serializer
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

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W24.objects
        if (
            instance.id_w24_parent
            and queryset.filter(pk=instance.id_w24_parent).exists()
        ):
            w24 = get_object_or_404(queryset, pk=instance.id_w24_parent)
            w24.status = "1"
            if not User.objects.filter(username=w24.username).exists():
                print("perform_destroy non trovo l'utente " + w24.username)
                w24.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w24.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W24.objects
        w24 = get_object_or_404(queryset, pk=pk)
        serializer = W24SerializerFull(w24, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # crea il nuovo bollettino di oggi

        now = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today.replace(hour=12, minute=30, second=0, microsecond=0)
        next_blt_time = emissione + datetime.timedelta(days=1)
        old = (
            models.W24.objects.filter(status="1").order_by("-last_update").latest("pk")
        )
        # gestione anno nuovo
        if old.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            last_seq_num_year = today.year
            new_seq = "1" + "/" + str(last_seq_num_year)
        else:
            last_seq_num = (
                models.W24.objects.filter(data_emissione__year=today.year)
                .exclude(status="0")
                .order_by("-last_update")[0]
                .numero_bollettino
            )
            last_seq_num_year = int(last_seq_num.split("/")[1])
            last_seq_num = last_seq_num.split("/")[0]
            print(last_seq_num)
            new_seq = str(int(last_seq_num) + 1)
            new_seq = str(new_seq) + "/" + str(last_seq_num_year)
        new = models.W24(
            numero_bollettino=new_seq,
            data_emissione=emissione,
            next_blt_time=next_blt_time,
            sintesi_meteo="",
            status=0,
            last_update=now,
            username=request.user,
            tipo_anomalia_termica="C",
            forzante_0="0",
            forzante_1="0",
            forzante_2="0",
        )
        new.save()

        print("created: ", new)
        print("creazione w24_data...")

        parametro = models.Parametro.objects.all().select_related("id_unita_misura")
        parametro_dict = {}
        for m in parametro:
            parametro_dict[m.id_parametro] = m

        areeAllertamento = models.AreeAllertamento.objects.all()
        areeAllertamento_dict = {}
        for mm in areeAllertamento:
            areeAllertamento_dict[str(mm.id_allertamento)] = mm

        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for mmm in time_layouts:
            time_layouts_dict[mmm.id_time_layouts] = mmm

        Aree = [
            "Piem-A",
            "Piem-B",
            "Piem-C",
            "Piem-D",
            "Piem-E",
            "Piem-F",
            "Piem-G",
            "Piem-H",
            "Piem-I",
            "Piem-L",
            "Piem-M",
        ]

        pioggia_tl = ["48", "66", "83"]

        giorni = {}

        giorni["48"] = ["45", "46"]
        giorni["66"] = ["60", "61", "62", "63"]
        giorni["83"] = ["77", "78", "79", "80"]

        today = datetime.datetime.today()
        data_emissione = today.replace(hour=12, minute=0, second=0, microsecond=0)

        riferimento_start = today.replace(hour=12, minute=0, second=0, microsecond=0)

        date_riferimento = [
            riferimento_start,
            riferimento_start.replace(hour=0, minute=0, second=0, microsecond=0)
            + datetime.timedelta(days=1),
            riferimento_start.replace(hour=0, minute=0, second=0, microsecond=0)
            + datetime.timedelta(days=2),
        ]

        date_to_tl_dict = {}
        date_to_tl_dict[date_riferimento[0]] = 48
        date_to_tl_dict[date_riferimento[1]] = 66
        date_to_tl_dict[date_riferimento[2]] = 83

        tl_to_date_dict = {}
        tl_to_date_dict["48"] = date_riferimento[0]
        tl_to_date_dict["66"] = date_riferimento[1]
        tl_to_date_dict["83"] = date_riferimento[2]

        print("Calcolo TEMPORALI")

        w30todayexists = False
        try:
            if W30.objects.filter(status="1"):
                if (
                    W30.objects.filter(status="1")
                    .filter(
                        data_emissione__year=today.year,
                        data_emissione__month=today.month,
                        data_emissione__day=today.day,
                    )
                    .latest("last_update")
                ):
                    latest_w30 = (
                        W30.objects.filter(status="1")
                        .filter(
                            data_emissione__year=today.year,
                            data_emissione__month=today.month,
                            data_emissione__day=today.day,
                        )
                        .latest("last_update")
                    )
                    if latest_w30.data_emissione.date() == today.date():
                        w30todayexists = True
                else:
                    w30todayexists = False
            else:
                w30todayexists = False
        except W30.DoesNotExist:
            print("ERRORE: Non trovo il PSA di oggi!")
            w30todayexists = False

        if w30todayexists:
            pluvs_125 = (
                W30Data.objects.filter(id_w30=latest_w30.id_w30)  # type: ignore
                .filter(id_aggregazione="125")
                .exclude(id_time_layouts="43")
                .exclude(id_time_layouts="44")
                .exclude(id_allertamento="Piem-V")
                .exclude(id_allertamento="Piem-T")
            )

            for area in Aree:
                for tl24h in pioggia_tl:
                    max6h = 0
                    for tl6h in giorni[tl24h]:
                        for pluv in pluvs_125.filter(id_time_layouts=tl6h).filter(  # type: ignore
                            id_allertamento=area
                        ):
                            if (
                                pluv.numeric_value is not None
                                and pluv.numeric_value > max6h
                            ):
                                max6h = pluv.numeric_value

                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=areeAllertamento_dict[area],
                        id_time_layouts=time_layouts_dict[int(tl24h)],
                        id_parametro=parametro_dict["CUM_PLUV"],
                        numeric_value=max6h,
                    )
                    new_data.save()

        else:
            for area in Aree:
                for tl24h in pioggia_tl:
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=areeAllertamento_dict[area],
                        id_time_layouts=time_layouts_dict[int(tl24h)],
                        id_parametro=parametro_dict["CUM_PLUV"],
                        numeric_value=0,
                    )
                    new_data.save()

        forecast_zone_VIG_IN_TH = models.ForecastZone.objects.filter(
            model_name="VIG_IN_TH"
        ).filter(data_emissione=data_emissione)

        if forecast_zone_VIG_IN_TH:
            stormtodayexists = True
        else:
            stormtodayexists = False

        if stormtodayexists:
            for area in Aree:
                for tl24h in pioggia_tl:
                    storm = (
                        forecast_zone_VIG_IN_TH.filter(id_allertamento=area)
                        .filter(data_riferimento=tl_to_date_dict[tl24h])
                        .get()
                    )
                    if storm.valore_originale is None:
                        valore_originale = Decimal(0)
                    else:
                        valore_originale = storm.valore_originale
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=areeAllertamento_dict[area],
                        id_time_layouts=time_layouts_dict[int(tl24h)],
                        id_parametro=parametro_dict["RISK_STORM"],
                        numeric_value=valore_originale,
                    )
                    new_data.save()
        else:
            for area in Aree:
                for tl24h in pioggia_tl:
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=areeAllertamento_dict[area],
                        id_time_layouts=time_layouts_dict[int(tl24h)],
                        id_parametro=parametro_dict["RISK_STORM"],
                        numeric_value=0,
                    )
                    new_data.save()

        print("Calcolo PRECIPITAZIONI")

        if w30todayexists:
            sogliepluv901 = models.W24Soglie.objects.filter(id_parametro="PLUV").filter(  # type: ignore
                id_aggregazione="901"
            )

            sogliepluv902 = models.W24Soglie.objects.filter(id_parametro="PLUV").filter(  # type: ignore
                id_aggregazione="902"
            )

            pluvs_902 = (
                W30Data.objects.filter(id_w30=latest_w30.id_w30)  # type: ignore
                .filter(id_aggregazione="902")
                .exclude(id_time_layouts="2010")
                .exclude(id_time_layouts="2011")
                .exclude(id_time_layouts="2014")
                .exclude(id_time_layouts="2015")
                .exclude(id_time_layouts="2016")
                .exclude(id_allertamento="Piem-V")
                .exclude(id_allertamento="Piem-T")
            )

            pluvs_901 = (
                W30Data.objects.filter(id_w30=latest_w30.id_w30)  # type: ignore
                .filter(id_aggregazione="901")
                .filter(id_time_layouts="48")
                .exclude(id_allertamento="Piem-V")
                .exclude(id_allertamento="Piem-T")
            )

            for pluv in pluvs_901:
                if pluv.numeric_value is None:
                    pluv_numeric_value = Decimal(0)
                else:
                    pluv_numeric_value = Decimal(pluv.numeric_value)
                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[
                        pluv.id_allertamento.id_allertamento
                    ],
                    id_time_layouts=time_layouts_dict[
                        pluv.id_time_layouts.id_time_layouts
                    ],
                    id_parametro=parametro_dict["PLUV"],
                    numeric_value=pluv_numeric_value,
                )
                new_data.save()

                areasoglie = sogliepluv901.filter(
                    id_allertamento=pluv.id_allertamento.id_allertamento
                )

                soglia01 = areasoglie.filter(classe_intensita="0").get().soglia1
                soglia02 = areasoglie.filter(classe_intensita="0").get().soglia2
                soglia11 = areasoglie.filter(classe_intensita="1").get().soglia1
                soglia12 = areasoglie.filter(classe_intensita="1").get().soglia2
                soglia21 = areasoglie.filter(classe_intensita="2").get().soglia1
                soglia22 = areasoglie.filter(classe_intensita="2").get().soglia2
                soglia31 = areasoglie.filter(classe_intensita="3").get().soglia1
                soglia32 = areasoglie.filter(classe_intensita="3").get().soglia2
                soglia41 = areasoglie.filter(classe_intensita="4").get().soglia1
                soglia42 = areasoglie.filter(classe_intensita="4").get().soglia2

                valore_classe = 0
                if pluv_numeric_value >= soglia01 and pluv_numeric_value <= soglia02:
                    valore_classe = 0
                if pluv_numeric_value >= soglia11 and pluv_numeric_value <= soglia12:
                    valore_classe = 1
                if pluv_numeric_value >= soglia21 and pluv_numeric_value <= soglia22:
                    valore_classe = 2
                if pluv_numeric_value >= soglia31 and pluv_numeric_value <= soglia32:
                    valore_classe = 3
                if pluv_numeric_value >= soglia41 and pluv_numeric_value <= soglia42:
                    valore_classe = 4

                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[
                        pluv.id_allertamento.id_allertamento
                    ],
                    id_time_layouts=time_layouts_dict[
                        pluv.id_time_layouts.id_time_layouts
                    ],
                    id_parametro=parametro_dict["RISK_RAIN"],
                    numeric_value=valore_classe,
                )
                new_data.save()

            for pluv in pluvs_902:
                if pluv.numeric_value is None:
                    pluv_numeric_value = Decimal(0)
                else:
                    pluv_numeric_value = Decimal(pluv.numeric_value)
                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[
                        pluv.id_allertamento.id_allertamento
                    ],
                    id_time_layouts=time_layouts_dict[
                        pluv.id_time_layouts.id_time_layouts
                    ],
                    id_parametro=parametro_dict["PLUV"],
                    numeric_value=pluv_numeric_value,
                )
                new_data.save()

                areasoglie = sogliepluv902.filter(
                    id_allertamento=pluv.id_allertamento.id_allertamento
                )

                soglia01 = areasoglie.filter(classe_intensita="0").get().soglia1
                soglia02 = areasoglie.filter(classe_intensita="0").get().soglia2
                soglia11 = areasoglie.filter(classe_intensita="1").get().soglia1
                soglia12 = areasoglie.filter(classe_intensita="1").get().soglia2
                soglia21 = areasoglie.filter(classe_intensita="2").get().soglia1
                soglia22 = areasoglie.filter(classe_intensita="2").get().soglia2
                soglia31 = areasoglie.filter(classe_intensita="3").get().soglia1
                soglia32 = areasoglie.filter(classe_intensita="3").get().soglia2
                soglia41 = areasoglie.filter(classe_intensita="4").get().soglia1
                soglia42 = areasoglie.filter(classe_intensita="4").get().soglia2

                valore_classe = 0
                if pluv_numeric_value >= soglia01 and pluv_numeric_value <= soglia02:
                    valore_classe = 0
                if pluv_numeric_value >= soglia11 and pluv_numeric_value <= soglia12:
                    valore_classe = 1
                if pluv_numeric_value >= soglia21 and pluv_numeric_value <= soglia22:
                    valore_classe = 2
                if pluv_numeric_value >= soglia31 and pluv_numeric_value <= soglia32:
                    valore_classe = 3
                if pluv_numeric_value >= soglia41 and pluv_numeric_value <= soglia42:
                    valore_classe = 4

                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[
                        pluv.id_allertamento.id_allertamento
                    ],
                    id_time_layouts=time_layouts_dict[
                        pluv.id_time_layouts.id_time_layouts
                    ],
                    id_parametro=parametro_dict["RISK_RAIN"],
                    numeric_value=valore_classe,
                )
                new_data.save()
        else:
            for area in Aree:
                for tl24h in pioggia_tl:
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=areeAllertamento_dict[area],
                        id_time_layouts=time_layouts_dict[int(tl24h)],
                        id_parametro=parametro_dict["PLUV"],
                        numeric_value=0,
                    )
                    new_data.save()

                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=areeAllertamento_dict[area],
                        id_time_layouts=time_layouts_dict[int(tl24h)],
                        id_parametro=parametro_dict["RISK_RAIN"],
                        numeric_value=0,
                    )
                    new_data.save()

        print("Calcolo ANOMALIA TERMICA")

        forecast_zone_ANOM_T_C = models.ForecastZone.objects.filter(
            model_name="ANOM_T_C"
        ).filter(data_emissione=data_emissione)

        forecast_zone_ANOM_T_F = models.ForecastZone.objects.filter(
            model_name="ANOM_T_F"
        ).filter(data_emissione=data_emissione)

        anomCaldoexists = False
        anomFreddoexists = False
        if forecast_zone_ANOM_T_C:
            anomCaldoexists = True
            anomFreddoexists = False
            w24 = models.W24.objects.get(pk=new.id_w24)
            setattr(w24, "tipo_anomalia_termica", "C")
            w24.save()
        elif forecast_zone_ANOM_T_F:
            anomFreddoexists = True
            anomCaldoexists = False
            w24 = models.W24.objects.get(pk=new.id_w24)
            setattr(w24, "tipo_anomalia_termica", "F")
            w24.save()
        else:
            anomCaldoexists = False
            anomFreddoexists = False

        freddo_tl = ["66", "83"]
        if anomCaldoexists:
            for data_riferimento in date_riferimento:
                for anomalia_c in forecast_zone_ANOM_T_C.filter(
                    data_riferimento=data_riferimento
                ):
                    if anomalia_c.valore_originale is None:
                        valore_originale = Decimal(0)
                    else:
                        valore_originale = Decimal(anomalia_c.valore_originale)
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=anomalia_c.id_allertamento,
                        id_time_layouts=time_layouts_dict[
                            date_to_tl_dict[data_riferimento]
                        ],
                        id_parametro=anomalia_c.id_parametro,
                        numeric_value=valore_originale,
                    )
                    new_data.save()

            allw24 = models.W24Data.objects.filter(id_w24=new)
            for time_layout in pioggia_tl:
                terma_datas = allw24.filter(id_time_layouts=time_layout).filter(  # type: ignore
                    id_parametro="TERMA"
                )
                terma1_datas = allw24.filter(id_time_layouts=time_layout).filter(  # type: ignore
                    id_parametro="TERMA1"
                )
                terma2_datas = allw24.filter(id_time_layouts=time_layout).filter(  # type: ignore
                    id_parametro="TERMA2"
                )

                for area in Aree:
                    terma_data = terma_datas.filter(id_allertamento=area).get()
                    terma1_data = terma1_datas.filter(id_allertamento=area).get()
                    terma2_data = terma2_datas.filter(id_allertamento=area).get()
                    if terma_data.numeric_value < terma1_data.numeric_value:
                        valore_classe = 0
                    if (
                        terma_data.numeric_value >= terma1_data.numeric_value
                        and terma_data.numeric_value < terma2_data.numeric_value
                    ):
                        valore_classe = 1
                    if terma_data.numeric_value >= terma2_data.numeric_value:
                        valore_classe = 2
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=terma_data.id_allertamento,
                        id_time_layouts=terma_data.id_time_layouts,
                        id_parametro=parametro_dict["RISK_THOT"],
                        numeric_value=valore_classe,
                    )
                    new_data.save()
        elif anomFreddoexists:
            for data_riferimento in date_riferimento:
                for anomalia_f in forecast_zone_ANOM_T_F.filter(
                    data_riferimento=data_riferimento
                ):
                    value = anomalia_f.valore_originale
                    if value is not None:
                        new_data = models.W24Data(
                            id_w24=new,
                            id_allertamento=anomalia_f.id_allertamento,
                            id_time_layouts=time_layouts_dict[
                                date_to_tl_dict[data_riferimento]
                            ],
                            id_parametro=anomalia_f.id_parametro,
                            numeric_value=value,
                        )
                        new_data.save()

            allw24 = models.W24Data.objects.filter(id_w24=new)

            for time_layout in freddo_tl:
                terma_datas = allw24.filter(id_time_layouts=time_layout).filter(  # type: ignore
                    id_parametro="TERMA"
                )
                terma1_datas = allw24.filter(id_time_layouts=time_layout).filter(  # type: ignore
                    id_parametro="TERMA1"
                )
                terma2_datas = allw24.filter(id_time_layouts=time_layout).filter(  # type: ignore
                    id_parametro="TERMA2"
                )
                for area in Aree:
                    terma_data = terma_datas.filter(id_allertamento=area).get()
                    terma1_data = terma1_datas.filter(id_allertamento=area).get()
                    terma2_data = terma2_datas.filter(id_allertamento=area).get()
                    if terma_data.numeric_value > terma1_data.numeric_value:
                        valore_classe = 0
                    if (
                        terma_data.numeric_value <= terma1_data.numeric_value
                        and terma_data.numeric_value > terma2_data.numeric_value
                    ):
                        valore_classe = 1
                    if terma_data.numeric_value <= terma2_data.numeric_value:
                        valore_classe = 2
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=terma_data.id_allertamento,
                        id_time_layouts=terma_data.id_time_layouts,
                        id_parametro=parametro_dict["RISK_TCOLD"],
                        numeric_value=valore_classe,
                    )
                    new_data.save()
        else:
            termas = ["TERMA", "TERMA1", "TERMA2"]
            year = today.year
            min = datetime.datetime(year, 10, 1)
            max = datetime.datetime(year + 1, 4, 30)
            tl_t = ["48", "66", "83"]
            if today.date() >= min.date() and today.date() <= max.date():
                termas.append("RISK_TCOLD")
                w24 = models.W24.objects.get(pk=new.id_w24)
                setattr(w24, "tipo_anomalia_termica", "F")
                w24.save()
                tl_t.pop(0)
            else:
                termas.append("RISK_THOT")
                w24 = models.W24.objects.get(pk=new.id_w24)
                setattr(w24, "tipo_anomalia_termica", "C")
                w24.save()

            for area in Aree:
                for tl24h in tl_t:
                    for terma in termas:
                        new_data = models.W24Data(
                            id_w24=new,
                            id_allertamento=areeAllertamento_dict[area],
                            id_time_layouts=time_layouts_dict[int(tl24h)],
                            id_parametro=parametro_dict[terma],
                            numeric_value=0,
                        )
                        new_data.save()

        print("Calcolo VENTO")
        forecast_zone_VIG_IN_WI = (
            models.ForecastZone.objects.filter(model_name="VIG_IN_WI")
            .filter(data_emissione=data_emissione)
            .exclude(id_allertamento="Piem-V")
            .exclude(id_allertamento="Piem-T")
        )

        sogliewind = models.W24Soglie.objects.filter(id_parametro="VELV")

        windexists = False
        if forecast_zone_VIG_IN_WI:
            windexists = True
        else:
            windexists = False

        if windexists:
            for data_riferimento in date_riferimento:
                for wind in forecast_zone_VIG_IN_WI.filter(
                    data_riferimento=data_riferimento
                ):
                    if wind.valore_originale is None:
                        valore_originale = Decimal(0)
                    else:
                        valore_originale = Decimal(wind.valore_originale)
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=wind.id_allertamento,
                        id_time_layouts=time_layouts_dict[
                            date_to_tl_dict[data_riferimento]
                        ],
                        id_parametro=parametro_dict["VELV"],
                        numeric_value=valore_originale,
                    )
                    new_data.save()

                    sogliearea = sogliewind.filter(
                        id_allertamento=wind.id_allertamento.id_allertamento
                    )
                    soglia01 = sogliearea.filter(classe_intensita="0").get().soglia1
                    soglia02 = sogliearea.filter(classe_intensita="0").get().soglia2
                    soglia11 = sogliearea.filter(classe_intensita="1").get().soglia1
                    soglia12 = sogliearea.filter(classe_intensita="1").get().soglia2
                    soglia21 = sogliearea.filter(classe_intensita="2").get().soglia1
                    soglia22 = sogliearea.filter(classe_intensita="2").get().soglia2

                    if valore_originale >= soglia01 and valore_originale <= soglia11:
                        valore_classe = 0
                    if valore_originale >= soglia11 and valore_originale <= soglia12:
                        valore_classe = 1
                    if valore_originale >= soglia21 and valore_originale <= soglia22:
                        valore_classe = 2

                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=wind.id_allertamento,
                        id_time_layouts=time_layouts_dict[
                            date_to_tl_dict[data_riferimento]
                        ],
                        id_parametro=parametro_dict["RISK_WIND"],
                        numeric_value=valore_classe,
                    )
                    new_data.save()
        else:
            winds = ["VELV", "RISK_WIND"]
            for area in Aree:
                for tl24h in pioggia_tl:
                    for wind1 in winds:
                        new_data = models.W24Data(
                            id_w24=new,
                            id_allertamento=areeAllertamento_dict[area],
                            id_time_layouts=time_layouts_dict[int(tl24h)],
                            id_parametro=parametro_dict[wind1],
                            numeric_value=0,
                        )
                        new_data.save()

        print("Calcolo NEBBIA e GELATE")
        risks = [
            "RISK_FOG",
            "RISK_FROST",
        ]
        classes_tl = ["48", "66", "83"]
        for timelayout in classes_tl:
            for risk in risks:
                for area in Aree:
                    new_data = models.W24Data(
                        id_w24=new,
                        id_allertamento=areeAllertamento_dict[area],
                        id_time_layouts=time_layouts_dict[int(timelayout)],
                        id_parametro=parametro_dict[risk],
                        numeric_value=0,
                    )
                    new_data.save()

        print("Calcolo PLUV e PLUV1")

        if w30todayexists:
            pluvs_900 = (
                W30Data.objects.filter(id_w30=latest_w30.id_w30)  # type: ignore
                .filter(id_aggregazione="900")
                .exclude(id_time_layouts="43")
                .exclude(id_time_layouts="44")
                .exclude(id_allertamento="Piem-V")
                .exclude(id_allertamento="Piem-T")
            )

            for pluv in pluvs_900:
                if pluv.numeric_value is None:
                    pluv_numeric_value = Decimal(0)
                else:
                    pluv_numeric_value = Decimal(pluv.numeric_value)
                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[
                        pluv.id_allertamento.id_allertamento
                    ],
                    id_time_layouts=time_layouts_dict[
                        pluv.id_time_layouts.id_time_layouts
                    ],
                    id_parametro=parametro_dict[pluv.id_parametro.id_parametro],
                    numeric_value=pluv_numeric_value,
                )
                new_data.save()

            for pluv in pluvs_125:
                if pluv.numeric_value is None:
                    pluv_numeric_value = Decimal(0)
                else:
                    pluv_numeric_value = Decimal(pluv.numeric_value)
                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[
                        pluv.id_allertamento.id_allertamento
                    ],
                    id_time_layouts=time_layouts_dict[
                        pluv.id_time_layouts.id_time_layouts
                    ],
                    id_parametro=parametro_dict["PLUV1"],
                    numeric_value=pluv_numeric_value,
                )
                new_data.save()

            print("Calcolo SNOW_LEV")

            snow_levels = (
                W30Data.objects.filter(id_w30=latest_w30.id_w30)  # type: ignore
                .filter(id_parametro="SNOW_LEV")
                .exclude(id_time_layouts="43")
                .exclude(id_time_layouts="44")
                .exclude(id_allertamento="Piem-V")
                .exclude(id_allertamento="Piem-T")
            )

            print("Calcolo SNOW_METERS")
            snow_meters = [400, 700, 1000, 2000]

            for snow_level in snow_levels:
                if snow_level.numeric_value is None:
                    snow_level_numeric_value = Decimal(0)
                else:
                    snow_level_numeric_value = Decimal(snow_level.numeric_value)
                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[
                        snow_level.id_allertamento.id_allertamento
                    ],
                    id_time_layouts=time_layouts_dict[
                        snow_level.id_time_layouts.id_time_layouts
                    ],
                    id_parametro=parametro_dict[snow_level.id_parametro.id_parametro],
                    numeric_value=snow_level_numeric_value,
                )
                new_data.save()

            zone_has_snow = {
                "SNOW_400": {
                    "Piem-A": True,
                    "Piem-B": False,
                    "Piem-C": False,
                    "Piem-D": False,
                    "Piem-E": False,
                    "Piem-F": True,
                    "Piem-G": True,
                    "Piem-H": True,
                    "Piem-I": True,
                    "Piem-L": True,
                    "Piem-M": True,
                },
                "SNOW_700": {
                    "Piem-A": True,
                    "Piem-B": True,
                    "Piem-C": True,
                    "Piem-D": True,
                    "Piem-E": True,
                    "Piem-F": True,
                    "Piem-G": True,
                    "Piem-H": True,
                    "Piem-I": False,
                    "Piem-L": False,
                    "Piem-M": True,
                },
                "SNOW_1000": {
                    "Piem-A": True,
                    "Piem-B": True,
                    "Piem-C": True,
                    "Piem-D": True,
                    "Piem-E": True,
                    "Piem-F": True,
                    "Piem-G": False,
                    "Piem-H": False,
                    "Piem-I": False,
                    "Piem-L": False,
                    "Piem-M": False,
                },
                "SNOW_2000": {
                    "Piem-A": True,
                    "Piem-B": True,
                    "Piem-C": True,
                    "Piem-D": True,
                    "Piem-E": True,
                    "Piem-F": True,
                    "Piem-G": False,
                    "Piem-H": False,
                    "Piem-I": False,
                    "Piem-L": False,
                    "Piem-M": False,
                },
            }

            for area in Aree:
                summedie = {}  # type: ignore
                for tl24h in pioggia_tl:
                    summedie[tl24h] = {}
                    summedie[tl24h]["400"] = 0
                    summedie[tl24h]["700"] = 0
                    summedie[tl24h]["1000"] = 0
                    summedie[tl24h]["2000"] = 0
                    for tl6h in giorni[tl24h]:
                        pluv = (
                            pluvs_900.filter(id_allertamento=area)  # type: ignore
                            .filter(id_time_layouts=tl6h)
                            .get()
                        )
                        if pluv.numeric_value is None:
                            pluv_numeric_value = Decimal(0)
                        else:
                            pluv_numeric_value = Decimal(pluv.numeric_value)

                        snow_level = (
                            snow_levels.filter(id_allertamento=area)  # type: ignore
                            .filter(id_time_layouts=tl6h)
                            .get()
                        )
                        if snow_level.numeric_value is None:
                            snow_level_numeric_value = Decimal(0)
                        else:
                            snow_level_numeric_value = Decimal(snow_level.numeric_value)

                        if snow_level_numeric_value <= 400:
                            summedie[tl24h]["400"] += pluv_numeric_value

                        if snow_level_numeric_value <= 700:
                            summedie[tl24h]["700"] += pluv_numeric_value

                        if snow_level_numeric_value <= 1300:
                            summedie[tl24h]["1000"] += pluv_numeric_value

                        if snow_level_numeric_value <= 2000:
                            summedie[tl24h]["2000"] += pluv_numeric_value

                    for mt in snow_meters:
                        if zone_has_snow["SNOW_" + str(mt)][
                            snow_level.id_allertamento.id_allertamento
                        ]:
                            new_data = models.W24Data(
                                id_w24=new,
                                id_allertamento=areeAllertamento_dict[
                                    snow_level.id_allertamento.id_allertamento
                                ],
                                id_time_layouts=time_layouts_dict[int(tl24h)],
                                id_parametro=parametro_dict["SNOW_" + str(mt)],
                                numeric_value=summedie[tl24h][str(mt)],
                            )
                            new_data.save()
                        else:
                            new_data = models.W24Data(
                                id_w24=new,
                                id_allertamento=areeAllertamento_dict[
                                    snow_level.id_allertamento.id_allertamento
                                ],
                                id_time_layouts=time_layouts_dict[int(tl24h)],
                                id_parametro=parametro_dict["SNOW_" + str(mt)],
                                numeric_value=0,
                            )
                            new_data.save()
        else:
            psaclasses = [
                "PLUV",
                "PLUV1",
                "SNOW_LEV",
            ]
            pluv_tl = ["45", "46", "60", "61", "62", "63", "77", "78", "79", "80"]

            for timelayout in pluv_tl:
                for param in psaclasses:
                    for area in Aree:
                        new_data = models.W24Data(
                            id_w24=new,
                            id_allertamento=areeAllertamento_dict[area],
                            id_time_layouts=time_layouts_dict[int(timelayout)],
                            id_parametro=parametro_dict[param],
                            numeric_value=0,
                        )
                        new_data.save()

            snowclasses = ["SNOW_400", "SNOW_700", "SNOW_1000", "SNOW_2000"]

            for timelayout in classes_tl:
                for snowmt in snowclasses:
                    for area in Aree:
                        new_data = models.W24Data(
                            id_w24=new,
                            id_allertamento=areeAllertamento_dict[area],
                            id_time_layouts=time_layouts_dict[int(timelayout)],
                            id_parametro=parametro_dict[snowmt],
                            numeric_value=0,
                        )
                        new_data.save()

        snow_400 = models.W24Data.objects.filter(id_w24=new.id_w24).filter(
            id_parametro="SNOW_400"
        )

        snow_700 = models.W24Data.objects.filter(id_w24=new.id_w24).filter(
            id_parametro="SNOW_700"
        )

        snow_1000 = models.W24Data.objects.filter(id_w24=new.id_w24).filter(
            id_parametro="SNOW_1000"
        )

        snow_2000 = models.W24Data.objects.filter(id_w24=new.id_w24).filter(
            id_parametro="SNOW_2000"
        )

        soglieneve = models.W24Soglie.objects.filter(id_parametro="SNOW")

        for area in Aree:
            for tlday in classes_tl:
                value_max = Decimal(0.0)

                value400 = (
                    snow_400.filter(id_allertamento=area)  # type: ignore
                    .filter(id_time_layouts=tlday)
                    .get()
                    .numeric_value
                )
                value700 = (
                    snow_700.filter(id_allertamento=area)  # type: ignore
                    .filter(id_time_layouts=tlday)
                    .get()
                    .numeric_value
                )
                value1000 = (
                    snow_1000.filter(id_allertamento=area)  # type: ignore
                    .filter(id_time_layouts=tlday)
                    .get()
                    .numeric_value
                )
                value2000 = (
                    snow_2000.filter(id_allertamento=area)  # type: ignore
                    .filter(id_time_layouts=tlday)
                    .get()
                    .numeric_value
                )

                v = [value400, value700, value1000, value2000]
                for value in v:
                    if value_max < value:
                        value_max = value

                aggregazione = 0
                if tlday == "48":
                    aggregazione = 901
                else:
                    aggregazione = 902

                areasoglie = soglieneve.filter(id_allertamento=area).filter(
                    id_aggregazione=aggregazione
                )

                print(areasoglie)

                soglia01 = areasoglie.filter(classe_intensita="0").get().soglia1
                soglia02 = areasoglie.filter(classe_intensita="0").get().soglia2
                soglia11 = areasoglie.filter(classe_intensita="1").get().soglia1
                soglia12 = areasoglie.filter(classe_intensita="1").get().soglia2
                soglia21 = areasoglie.filter(classe_intensita="2").get().soglia1
                soglia22 = areasoglie.filter(classe_intensita="2").get().soglia2
                soglia31 = areasoglie.filter(classe_intensita="3").get().soglia1
                soglia32 = areasoglie.filter(classe_intensita="3").get().soglia2

                valore_classe = 0
                if value_max >= soglia01 and value_max <= soglia02:
                    valore_classe = 0
                if value_max >= soglia11 and value_max <= soglia12:
                    valore_classe = 1
                if value_max >= soglia21 and value_max <= soglia22:
                    valore_classe = 2
                if value_max >= soglia31 and value_max <= soglia32:
                    valore_classe = 3

                new_data = models.W24Data(
                    id_w24=new,
                    id_allertamento=areeAllertamento_dict[area],
                    id_time_layouts=time_layouts_dict[int(tlday)],
                    id_parametro=parametro_dict["SNOW"],
                    numeric_value=valore_classe,
                )
                new_data.save()

        datiMancanti = ""
        print(anomCaldoexists, anomFreddoexists, windexists, w30todayexists)
        if (
            not stormtodayexists
            or (not anomCaldoexists and not anomFreddoexists)
            or not windexists
            or not w30todayexists
        ):
            datiMancanti += "|||InputDataIsMissing||| "
        if not stormtodayexists:
            datiMancanti += "ATTENZIONE: dati mancanti per temporali "
        if not anomCaldoexists and not anomFreddoexists:
            datiMancanti += "ATTENZIONE: dati mancanti per le anomalie termiche "
        if not windexists:
            datiMancanti += "ATTENZIONE: dati mancanti per vento "
        if not w30todayexists:
            datiMancanti += "ATTENZIONE: dati mancanti PSA"

        w24 = models.W24.objects.get(pk=new.id_w24)
        setattr(w24, "sintesi_meteo", datiMancanti)
        w24.save()

        return Response({"id_w24": new.id_w24})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w24/data/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w24 = next(s["id"] for s in snapshots if s["id_key"] == "id_w24")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w24",
            "id": id_w24,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w24 = models.W24.objects.get(pk=id_w24)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w24":
                print(
                    "id_w24:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                setattr(w24, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                print(
                    "id_w24_data:",
                    snapshot["id"],
                    "numeric_value",
                    snapshot["new_value"],
                )
                data = models.W24Data.objects.get(pk=snapshot["id"])
                data.numeric_value = snapshot["new_value"]
                data.save()
                updated += 1
        w24.save()
        fine = datetime.datetime.now()
        serializer = W24SerializerFull(w24, context={"request": request})
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
        old = models.W24.objects.get(pk=pk)
        print("w24 reopen:", old)
        old.status = "2"
        old_id_w24 = old.id_w24
        old.save()
        new_seq = int(old.numero_bollettino.split("/")[0]) + 1
        anno = int(old.numero_bollettino.split("/")[1])
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.numero_bollettino = f"{new_seq}/{anno}"
        new.last_update = now
        new.username = request.user
        new.id_w24_parent = old_id_w24
        new.save()
        old_data = models.W24Data.objects.filter(id_w24=old_id_w24)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w24 = new
            new_data.save()
        return Response({"id_w24": new.id_w24})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w24 = models.W24.objects.get(pk=pk)
        w24.status = "1"
        w24.username = request.user.username
        w24.last_update = inizio
        w24.save()

        today = datetime.datetime.today()
        data_emissione = today.replace(hour=12, minute=0, second=0, microsecond=0)

        old_forecast_zone = models.ForecastZone.objects.filter(
            data_emissione=data_emissione
        ).filter(model_name="VIGIL_W24")

        old_forecast_zone.delete()
        print("==============ELIMINAZIONE VECCHI DATI============")

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

        start = today.replace(hour=12, minute=0, second=0, microsecond=0)
        vig_time_layouts = [48, 66, 83]

        date_riferimento = {}
        for vig_tl in vig_time_layouts:
            time_layout = time_layouts_dict[vig_tl]
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
            date_riferimento[str(vig_tl)] = end_time

        risk_storm_w24 = models.W24Data.objects.filter(id_w24=w24.id_w24).filter(
            id_parametro="RISK_STORM"
        )

        for w24data in risk_storm_w24:
            newforecastzone = models.ForecastZone(
                id_allertamento=w24data.id_allertamento,
                id_parametro=w24data.id_parametro,
                id_aggregazione=aggregazione_dict["0"],
                model_type="DMO",
                model_name="VIGIL_W24",
                data_emissione=data_emissione,
                data_riferimento=date_riferimento[
                    str(w24data.id_time_layouts.id_time_layouts)
                ],
                valore_originale=w24data.numeric_value,
                valore_validato=None,
                last_update=inizio,
                username=request.user.username,
            )
            newforecastzone.save()

        snow_400_w24 = models.W24Data.objects.filter(id_w24=w24.id_w24).filter(
            id_parametro="SNOW_400"
        )

        snow_700_w24 = models.W24Data.objects.filter(id_w24=w24.id_w24).filter(
            id_parametro="SNOW_700"
        )

        snow_1000_w24 = models.W24Data.objects.filter(id_w24=w24.id_w24).filter(
            id_parametro="SNOW_1000"
        )

        snow_meters = [snow_400_w24, snow_700_w24, snow_1000_w24]

        tomorrow = start + datetime.timedelta(days=1)
        aftertomorrow = start + datetime.timedelta(days=2)
        snow_date_riferimento = {
            "48": start,
            "66": tomorrow.replace(hour=0, minute=0, second=0, microsecond=0),
            "83": aftertomorrow.replace(hour=0, minute=0, second=0, microsecond=0),
        }

        for snow_meter in snow_meters:
            for w24data in snow_meter:
                print(w24data.id_parametro)
                newforecastzone = models.ForecastZone(
                    id_allertamento=w24data.id_allertamento,
                    id_parametro=w24data.id_parametro,
                    id_aggregazione=aggregazione_dict["0"],
                    model_type="DMO",
                    model_name="VIGIL_W24",
                    data_emissione=data_emissione,
                    data_riferimento=snow_date_riferimento[
                        str(w24data.id_time_layouts.id_time_layouts)
                    ],
                    valore_originale=w24data.numeric_value,
                    valore_validato=None,
                    last_update=inizio,
                    username=request.user.username,
                )
                newforecastzone.save()

        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("vigilanza", w24.id_w24)
        return Response({"id_w24": w24.id_w24})


class W24CurrentView(RetrieveAPIView):
    """
    View the latest W24 bulletin sent for a certain day
    """

    queryset = models.W24.objects.filter(status="1").order_by("-last_update")
    serializer_class = W24SerializerFull
    lookup_field = "data_emissione"


class W24DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W24 bulletin Data to be viewed or edited
    """

    queryset = models.W24Data.objects.all()
    serializer_class = W24DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class MyFilter(filters.FilterSet):
    class Meta:
        model = models.ForecastZone
        fields = ["id_parametro"]


class ForecastZoneView(viewsets.ModelViewSet):
    queryset = models.ForecastZone.objects.all()
    serializer_class = ForecastZoneSerializer
    filterset_class = MyFilter
    permission_classes = [ReadOnly]


class W24SoglieView(viewsets.ModelViewSet):
    """
    API endpoint that allows W24 bulletin Data to be viewed or edited
    """

    queryset = models.W24Soglie.objects.all()
    serializer_class = W24SoglieSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


def rearrange(time_layout, key):
    rearranged = {}
    if key in time_layout:
        for record in time_layout[key]:
            code = record["id_allertamento"][5:]
            rearranged[code] = record
        time_layout[key] = rearranged


def rearrange_risks(time_layout):
    rearrange(time_layout, "RISK_RAIN")
    rearrange(time_layout, "RISK_THOT")
    rearrange(time_layout, "RISK_TCOLD")
    rearrange(time_layout, "RISK_FROST")
    rearrange(time_layout, "RISK_FOG")
    rearrange(time_layout, "SNOW")
    rearrange(time_layout, "RISK_STORM")
    rearrange(time_layout, "RISK_WIND")


icon_anchors = {
    "A": [200, 65],
    "B": [150, 150],
    "C": [30, 250],
    "D": [-35, 370],
    "E": [-30, 507],
    "F": [116, 520],
    "G": [215, 420],
    "H": [293, 372],
    "I": [190, 238],
    "L": [90, 320],
    "M": [68, 430],
}


class VigilanzaHTMLView(TemplateView):
    template_name = "vigilanza.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W24.objects
        w24 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W24SerializerFull(w24)
        vigilanza = serializer.data

        convert_to_date(vigilanza, "next_blt_time")
        convert_to_date(vigilanza, "data_emissione")

        for data in vigilanza["w24data_set"]:
            if data["id_time_layouts"] not in vigilanza:
                vigilanza[data["id_time_layouts"]] = {}
            if data["id_parametro"] in vigilanza[data["id_time_layouts"]]:
                vigilanza[data["id_time_layouts"]][data["id_parametro"]].append(data)
            else:
                vigilanza[data["id_time_layouts"]][data["id_parametro"]] = [data]
        rearrange_risks(vigilanza[48])
        rearrange_risks(vigilanza[66])
        rearrange_risks(vigilanza[83])

        giorni = {}
        giorni["48"] = ["45", "46"]
        giorni["66"] = ["60", "61", "62", "63"]
        giorni["83"] = ["77", "78", "79", "80"]

        obj = {
            "A": "",
            "B": "",
            "C": "",
            "D": "",
            "E": "",
            "F": "",
            "G": "",
            "H": "",
            "I": "",
            "L": "",
            "M": "",
        }

        quote_neve = {}  # type: ignore
        count_icons = {}  # type: ignore

        classes = ["RISK_FROST", "RISK_FOG", "SNOW", "RISK_STORM", "RISK_WIND"]

        if "RISK_THOT" in vigilanza[48]:
            classes.append("RISK_THOT")
        else:
            classes.append("RISK_TCOLD")

        print(classes)
        for tlday in giorni:
            for tl in giorni[tlday]:
                rearrange(vigilanza[int(tl)], "SNOW_LEV")
                rearrange(vigilanza[int(tl)], "PLUV")

        for tlday in giorni:
            quote_neve[str(tlday)] = {}
            count_icons[str(tlday)] = {}
            for area in obj:
                max = 0
                min = 6000
                count_icons[str(tlday)][area] = 0
                quote_neve[str(tlday)][area] = ""

                for classe in classes:
                    if not (tlday == "48" and classe == "RISK_TCOLD"):
                        if (
                            int(
                                float(
                                    vigilanza[int(tlday)][classe][area]["numeric_value"]
                                )
                            )
                            > 0
                        ):
                            count_icons[str(tlday)][area] += 1

                for tl in giorni[tlday]:
                    if (
                        int(float(vigilanza[int(tl)]["PLUV"][area]["numeric_value"]))
                        > 0
                    ):
                        if max < int(
                            float(vigilanza[int(tl)]["SNOW_LEV"][area]["numeric_value"])
                        ):
                            max = int(
                                float(
                                    vigilanza[int(tl)]["SNOW_LEV"][area][
                                        "numeric_value"
                                    ]
                                )
                            )
                        if min > int(
                            float(vigilanza[int(tl)]["SNOW_LEV"][area]["numeric_value"])
                        ):
                            min = int(
                                float(
                                    vigilanza[int(tl)]["SNOW_LEV"][area][
                                        "numeric_value"
                                    ]
                                )
                            )

                if min == max or min == 6000:
                    quote_neve[str(tlday)][area] = str(max)
                else:
                    quote_neve[str(tlday)][area] = str(min) + "-" + str(max)

        textpx = {}  # type: ignore
        imgpx = {}  # type: ignore
        for tl in count_icons:
            textpx[tl] = {}
            imgpx[tl] = {}
            for area in count_icons[tl]:
                if count_icons[tl][area] < 4:
                    imgpx[tl][area] = "0px"
                    textpx[tl][area] = "44px"
                else:
                    imgpx[tl][area] = "25px"
                    textpx[tl][area] = "72px"

        print(count_icons)
        vigilanza.pop("w24data_set")

        today = vigilanza["data_emissione"]
        tomorrow = vigilanza["data_emissione"] + datetime.timedelta(days=1)
        aftertomorrow = vigilanza["data_emissione"] + datetime.timedelta(days=2)

        print(today)
        context = {
            "vigilanza": vigilanza,
            "icon_anchors": icon_anchors,
            "quote_neve": quote_neve,
            "textpx": textpx,
            "imgpx": imgpx,
            "dates": [
                today,
                tomorrow,
                aftertomorrow,
            ],
        }
        return context


class VigilanzaPDFView(VigilanzaHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="vigilanza.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class VigilanzaPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w24/pdf/%d" % kwargs["pk"])

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


class VigilanzaPngRuparView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w24/rupar_pdf/%d" % kwargs["pk"])

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
