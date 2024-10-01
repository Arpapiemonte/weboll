#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
import math
from collections import OrderedDict

# import locale
from io import BytesIO

import numpy as np

# import tempfile
# from contextlib import closing
# from subprocess import call
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db.transaction import atomic
from django.http import JsonResponse

# from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from matplotlib import pyplot as plt
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView

# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w35.back import models as models_w35
from w36.back import models
from w36.back.serializers import (
    W36DataSerializer,
    W36ParametriEquazioneSerializer,
    W36Serializer,
    W36SerializerFull,
)
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core import models as models_w05


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class ChartView(View):
    def get(self, request, *args, **kwargs):
        queryset = models.W36.objects
        w36 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W36SerializerFull(w36)
        mpa = serializer.data
        graphic_max = mpa["chart_max"]
        graphic_min = mpa["chart_min"]
        return JsonResponse({"graphic_max": graphic_max, "graphic_min": graphic_min})


class W36ParametriEquazioneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W36 parametri equazione to be viewed
    """

    queryset = models.W36ParametriEquazione.objects.all()
    serializer_class = W36ParametriEquazioneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W36View(viewsets.ModelViewSet):
    """
    API endpoint that allows W36 bulletins to be viewed or edited
    """

    queryset = models.W36.objects.order_by("-last_update", "-pk")
    serializer_class = W36Serializer
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
        queryset = models.W36.objects
        w36 = get_object_or_404(queryset, pk=pk)
        serializer = W36SerializerFull(w36, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W36.objects
        if (
            instance.id_w36_parent
            and queryset.filter(pk=instance.id_w36_parent).exists()
        ):
            w36 = get_object_or_404(queryset, pk=instance.id_w36_parent)
            w36.status = "1"
            if not User.objects.filter(username=w36.username).exists():
                print("perform_destroy non trovo l'utente " + w36.username)
                w36.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w36.save()
        instance.delete()

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w36 = models.W36.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w36.id_w36,
            "del",
            w36.data_emissione,
            "iniziato",
        )
        w36.status = "1"
        w36.username = request.user.username
        w36.last_update = inizio
        w36.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("ondatecalore", w36.id_w36)
        return Response({"id_w36": w36.id_w36})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send_auto(self, request, pk):
        w36 = models.W36.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w36.id_w36,
            "del",
            w36.data_emissione,
            "iniziato",
        )
        send_with_celery("ondatecalore", w36.id_w36, True)
        return Response({"id_w36": w36.id_w36})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        delimiter = "__"

        # hash meteo_real_time
        def HashMRT(codice_istat_comune, progr_punto_com, id_parametro, data, ora):
            epoch_time = datetime.datetime.strptime(
                str(data) + " " + str(ora), "%Y-%m-%d %H:%M:%S"
            ).timestamp()
            return (
                str(codice_istat_comune)
                + delimiter
                + str(progr_punto_com)
                + delimiter
                + str(id_parametro)
                + delimiter
                + str(epoch_time)
            )

        def filterMRT(
            mrt_dict,
            size,
            codice_istat_comune,
            progr_punto_com,
            id_parametro,
            inizio,
            fine,
            dayago,
        ):
            result = np.full(size, np.nan)
            for mrt in mrt_dict:
                epoch_time = float(mrt.split(delimiter)[3])
                # print(mrt_dict[mrt]["codice_istat_comune"],mrt_dict[mrt]["progr_punto_com"],
                # mrt_dict[mrt]["id_parametro"], epoch_time, inizio, fine)
                if (
                    mrt_dict[mrt]["codice_istat_comune"] == codice_istat_comune
                    and str(mrt_dict[mrt]["progr_punto_com"]) == progr_punto_com
                    and mrt_dict[mrt]["id_parametro"] == id_parametro
                    and epoch_time >= inizio
                    and epoch_time <= fine
                ):
                    """
                    print(
                        "filterMRT",
                        codice_istat_comune,
                        progr_punto_com,
                        id_parametro,
                        "OGGETTO",
                        dayago,
                        mrt_dict[mrt]["data"],
                        mrt_dict[mrt]["ora"],
                        mrt_dict[mrt]["valore_validato"],
                    )
                    """
                    result[int((epoch_time - inizio) / 1800)] = mrt_dict[mrt][
                        "valore_validato"
                    ]
            return result

        def HashW36Data(id_venue, id_time_layouts, id_parametro, id_aggregazione):
            return (
                str(id_venue)
                + delimiter
                + str(id_time_layouts)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
            )

        # hash forecast_values
        def HashFV(cod_staz_meteo, id_parametro, id_aggregazione, data, ora):
            epoch_time = datetime.datetime.strptime(
                str(data) + " " + str(ora), "%Y-%m-%d %H:%M:%S"
            ).timestamp()
            return (
                cod_staz_meteo
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(epoch_time)
            )

        def filterFV(fv_dict, size, cod_staz_meteo, id_parametro, inizio, fine, dayago):
            result = np.full(size, np.nan)
            for fv in fv_dict:
                epoch_time = float(fv.split(delimiter)[3])
                if (
                    fv_dict[fv].id_forecast_parameter.id_forecast_station.cod_staz_meteo
                    == cod_staz_meteo
                    and fv_dict[fv].id_forecast_parameter.id_parametro.id_parametro
                    == id_parametro
                    and epoch_time >= inizio
                    and epoch_time <= fine
                ):
                    """
                    print(
                        "filterFV",
                        cod_staz_meteo,
                        id_parametro,
                        "OGGETTO",
                        dayago,
                        fv_dict[fv].date_rif,
                        fv_dict[fv].time_rif,
                        fv_dict[fv].value,
                    )
                    """
                    result[int((epoch_time - inizio) / 3600)] = fv_dict[fv].value
            return result

        w36_json = {}

        today = datetime.datetime.now()
        # today = datetime.datetime(2024, 7, 31)
        inizio = datetime.datetime.now()
        emissione = today
        old_w36 = None
        if (
            models.W36.objects.filter(status="1")
            .filter(data_emissione__year=today.year)
            .order_by("-last_update")
            .exists()
        ):
            old_w36 = (
                models.W36.objects.filter(status="1")
                .filter(data_emissione__year=today.year)
                .order_by("-last_update")
                .latest("pk")
            )
        if old_w36 is not None:
            print(
                "new del bollettino ",
                old_w36.id_w36,
                "del",
                old_w36.data_emissione,
                "iniziato",
            )
            # aumento il sequenziale perchè è una nuova emissione
            seq_num = int(old_w36.seq_num)  # type: ignore
            seq_num = seq_num + 1
        else:
            seq_num = 1
        new = models.W36(
            data_emissione=emissione.date(),
            status="X",
            last_update=datetime.datetime.now(),
            username=request.user,
            seq_num=str(seq_num),
        )
        new.save()

        w36_json["data_emissione"] = datetime.datetime.strftime(
            emissione.date(), "%Y-%m-%d"
        )
        w36_json["status"] = "X"
        w36_json["last_update"] = datetime.datetime.now().isoformat()
        w36_json["username"] = request.user
        w36_json["seq_num"] = str(seq_num)

        fine = datetime.datetime.now()
        print(
            "leggo venues ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        venues = models.Venue.objects.all()
        venues_dict = {}
        for v in venues:
            venues_dict[str(v.id_venue)] = v
        fine = datetime.datetime.now()
        print(
            "leggo parametro ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        parametri = models.Parametro.objects.all().select_related("id_unita_misura")
        parametri_dict = {}
        for p in parametri:
            parametri_dict[p.id_parametro] = p
        fine = datetime.datetime.now()
        print(
            "leggo aggregazione ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        aggregazione = models.Aggregazione.objects.all().select_related(
            "id_unita_misura"
        )
        aggregazione_dict = {}
        for a in aggregazione:
            aggregazione_dict[str(a.id_aggregazione)] = a
        fine = datetime.datetime.now()
        print(
            "leggo time_layouts ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for t in time_layouts:
            time_layouts_dict[str(t.id_time_layouts)] = t
        fine = datetime.datetime.now()
        print(
            "leggo classes ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )

        # creo il dizionario del w36_data vuoto
        with open("config/w36_data.json") as json_file:
            w36_data_config = json.load(json_file)
        w36_data_dict = {}
        for w36_dc in w36_data_config:
            # print(w36_dc)
            w36_data_dict[
                HashW36Data(
                    w36_dc["id_venue"],
                    w36_dc["id_time_layouts"],
                    w36_dc["id_parametro"],
                    w36_dc["id_aggregazione"],
                )
            ] = models.W36Data(
                id_w36=new,
                id_venue=venues_dict[str(w36_dc["id_venue"])],
                id_time_layouts=time_layouts_dict[str(w36_dc["id_time_layouts"])],
                id_parametro=parametri_dict[w36_dc["id_parametro"]],
                id_aggregazione=aggregazione_dict[str(w36_dc["id_aggregazione"])],
                numeric_value=None,
            )

        stazioni = [
            "94061",  # giardini reali
            "93447",  # consolata
            "90115",  # alessandria lobbi
            "94194",  # asti penna
            "90198",  # vercelli
            "90641",  # pallanza
            "94193",  # novara
            "93254",  # cuneo cascina vecchia
            "92891",  # cuneo camera commercio
            "92566",  # biella
        ]
        venue2stazione = {
            59: [  # torino
                "94061",  # giardini reali
                "94061",  # giardini reali
                "93447",  # consolata
            ],
            9: [  # alessandria
                "90115",  # alessandria lobbi
                "90115",  # alessandria lobbi
                "90115",  # alessandria lobbi
            ],
            11: [  # asti
                "94194",  # asti penna
                "94194",  # asti penna
                "94194",  # asti penna
            ],
            64: [  # vercelli
                "90198",  # vercelli
                "90198",  # vercelli
                "90198",  # vercelli
            ],
            63: [  # verbania
                "90641",  # pallanza
                "90641",  # pallanza
                "90641",  # pallanza
            ],
            33: [  # novara
                "94193",  # novara
                "94193",  # novara
                "94193",  # novara
            ],
            28: [  # cuneo
                "93254",  # cuneo cascina vecchia
                "93254",  # cuneo cascina vecchia
                "92891",  # cuneo camera commercio
            ],
            1: [  # biella
                "92566",  # biella
                "92566",  # biella
                "92566",  # biella viene resettato a 1 oerchè non c'è anemometro
            ],
        }
        id_venue2name = {
            "59": "Torino",
            "9": "Alessandria",
            "11": "Asti",
            "64": "Vercelli",
            "63": "Verbania",
            "33": "Novara",
            "28": "Cuneo",
            "1": "Biella",
        }
        osservati = "venue;data;parametro;terma;igro;velv;at;75;90;95"
        debug = ""
        at_dict = {}  # type: ignore
        my_days_ago = 8

        # leggo i percentili per stamparli negli osservati
        mesi = []
        giorni = []
        mmgg = []
        for day in range(-my_days_ago, 1):
            giorno = today + datetime.timedelta(days=day)
            mmgg.append(str(giorno.month) + "_" + str(giorno.day))
            giorni.append(str(giorno.day))
            mesi.append(str(giorno.month))

        w36_percentili = (
            models.W36Percentili.objects.filter(mese__in=mesi)
            .filter(giorno__in=giorni)
            .order_by("id_venue", "mese", "giorno")
        )
        percentili_dict = {}
        for w36_p in w36_percentili:
            percentili_dict[
                str(w36_p.id_venue.id_venue)
                + delimiter
                + str(w36_p.mese)
                + delimiter
                + str(w36_p.giorno)
                + delimiter
                + str(w36_p.id_parametro.id_parametro)
                + delimiter
                + str(w36_p.id_aggregazione.id_aggregazione)
            ] = w36_p.numeric_value
        # print("percentili_dict", percentili_dict)

        # cerco tutti i codici istat comune e progr punto com in base ai cod_staz_meteo
        stazione_misura_dict = {}
        stazione_misuras = models_w05.StazioneMisura.objects.exclude(
            cod_staz_meteo=None
        )
        for stazione_misura in stazione_misuras:
            stazione_misura_dict[stazione_misura.cod_staz_meteo] = stazione_misura

        codice_istat_comunes = []
        progr_punto_coms = []
        parametri = ["TERMA", "IGRO", "VELV"]  # type: ignore
        for venue in venue2stazione:
            for idx, csm in enumerate(venue2stazione[venue]):
                id_parametro = parametri[idx]
                codice_istat_comunes.append(
                    stazione_misura_dict[csm].codice_istat_comune.codice_istat_comune
                )
                progr_punto_coms.append(stazione_misura_dict[csm].progr_punto_com)

        # salvo in memoria i valori osservati ogni 30 minuti
        fivedaysago = today - datetime.timedelta(days=my_days_ago)
        mrts = (
            models.MeteoRealTime.objects.values(
                "codice_istat_comune",
                "progr_punto_com",
                "data",
                "ora",
                "id_parametro",
                "valore_validato",
            )
            .filter(id_parametro__in=parametri)
            .filter(codice_istat_comune__in=codice_istat_comunes)
            .filter(progr_punto_com__in=progr_punto_coms)
            .filter(data__gte=fivedaysago)
            .filter(tipologia_validaz="OK")
            .filter(flag_validaz_autom=0)
            .filter(id_aggregazione=0)
            .filter(Q(ora__contains="00:00") | Q(ora__contains="30:00"))
            .order_by(
                "codice_istat_comune", "progr_punto_com", "data", "ora", "id_parametro"
            )
        )
        mrt_dict = {}
        for mrt in mrts:
            mrt_dict[
                HashMRT(
                    mrt["codice_istat_comune"],
                    mrt["progr_punto_com"],
                    mrt["id_parametro"],
                    mrt["data"],
                    mrt["ora"],
                )
            ] = mrt

        tl = {-4: 301, -3: 300, -2: 15, -1: 32, 0: 48}
        # ex_tl = [301, 300, 15, 32, 48]
        giorni_di_caldo = {}  # type: ignore
        for parametro in ["min", "max"]:
            for dayago in range(my_days_ago):
                size = 25
                if parametro == "min":
                    inizio = (
                        today - datetime.timedelta(days=my_days_ago - dayago)
                    ).replace(hour=18, minute=0, second=0, microsecond=0)
                    # print("inizio", dayago, inizio)
                    fine = (
                        today - datetime.timedelta(days=(my_days_ago - 1) - dayago)
                    ).replace(hour=6, minute=0, second=0, microsecond=0)
                    # print("fine", dayago, fine)
                if parametro == "max":
                    inizio = (
                        today - datetime.timedelta(days=(my_days_ago - 1) - dayago)
                    ).replace(hour=6, minute=0, second=0, microsecond=0)
                    # print("inizio", dayago, inizio)
                    fine = (
                        today - datetime.timedelta(days=(my_days_ago - 1) - dayago)
                    ).replace(hour=18, minute=0, second=0, microsecond=0)
                    # print("fine", dayago, fine)
                inizio_date = inizio
                fine_date = fine
                inizio = inizio.timestamp()  # type: ignore
                fine = fine.timestamp()  # type: ignore
                for venue in venue2stazione:
                    # print("########### inizio venue", venue)
                    id_venue = str(venue)
                    for idx, csm in enumerate(venue2stazione[venue]):
                        id_parametro = parametri[idx]
                        codice_istat_comune = stazione_misura_dict[
                            csm
                        ].codice_istat_comune.codice_istat_comune
                        progr_punto_com = str(stazione_misura_dict[csm].progr_punto_com)
                        # denominazione = stazione_misura_dict[csm].denominazione
                        """
                        print(
                            "----- carico i dati per",
                            id_venue,
                            denominazione,
                            codice_istat_comune,
                            progr_punto_com,
                            id_parametro,
                            parametro,
                            tl[dayago],
                        )
                        """

                        if id_parametro == "TERMA":
                            terma = filterMRT(
                                mrt_dict,
                                size,
                                codice_istat_comune,
                                progr_punto_com,
                                id_parametro,
                                inizio,
                                fine,
                                dayago,
                            )
                            """
                            print(
                                "terma",
                                codice_istat_comune,
                                progr_punto_com,
                                dayago,
                                terma,
                            )
                            """

                        if id_parametro == "IGRO":
                            igro = filterMRT(
                                mrt_dict,
                                size,
                                codice_istat_comune,
                                progr_punto_com,
                                id_parametro,
                                inizio,
                                fine,
                                dayago,
                            )
                            # print("igro", dayago, igro)

                        if "VEL" in id_parametro:  # type: ignore
                            velv = filterMRT(
                                mrt_dict,
                                size,
                                codice_istat_comune,
                                progr_punto_com,
                                id_parametro,
                                inizio,
                                fine,
                                dayago,
                            )
                            # print("velv", dayago, velv)
                            if np.isnan(velv).all():
                                # inizializzo l'array con la velocità vento 1 m/s
                                print(
                                    id_venue
                                    + " "
                                    + codice_istat_comune
                                    + " "
                                    + progr_punto_com
                                    + " VELV non ha dati setto tutto l'array con valori di 1 m/s!"
                                )
                                velv = np.full(size, 1)
                                # print("velv", dayago, velv)
                    """
                    print(
                        "----- colcolo e salvo le AT per",
                        id_venue,
                        denominazione,
                        codice_istat_comune,
                        progr_punto_com,
                        id_parametro,
                        parametro,
                        tl[dayago],
                    )
                    """
                    e = 6.112 * 10 ** ((7.5 * terma) / (237.7 + terma)) * igro / 100
                    at = -2.7 + 1.04 * terma + 2 * e / 10 - 0.65 * velv
                    """
                    print("")
                    print(
                        "Temperatura apparente",
                        venue,
                        parametro,
                        dayago,
                        at,
                        inizio_date,
                        fine_date,
                        tl[dayago],
                    )
                    print("")
                    """
                    k = 0
                    start_date = inizio_date
                    perc_array = []
                    while start_date <= fine_date:
                        param = "AT" + parametro.upper()
                        for aggreg in [940, 941, 942]:
                            perc_key = (
                                str(id_venue)
                                + delimiter
                                + str(start_date.month)
                                + delimiter
                                + str(start_date.day)
                                + delimiter
                                + str(param)
                                + delimiter
                                + str(aggreg)
                            )
                            # print("cerco percentili per il giorno", perc_key)
                            perc_array.append(percentili_dict[perc_key])
                        osservati = (
                            osservati
                            + "\n"
                            + id_venue2name[str(id_venue)]
                            + ";"
                            + start_date.strftime("%Y-%m-%d %H:%M")
                            + ";"
                            + param
                            + ";"
                            + str(terma[k])
                            + ";"
                            + str(igro[k])
                            + ";"
                            + str(velv[k])
                            + ";"
                            + str(round(at[k], 2))
                            + ";"
                            + str(perc_array[0])
                            + ";"
                            + str(perc_array[1])
                            + ";"
                            + str(perc_array[2])
                        )
                        at_dict_key = (
                            id_venue + delimiter + fine_date.strftime("%Y-%m-%d")
                        )
                        if at_dict_key not in at_dict:
                            at_dict[at_dict_key] = {}
                        if param == "ATMAX":
                            at_dict[at_dict_key]["percmax"] = float(perc_array[0])  # type: ignore
                        if param == "ATMIN":
                            at_dict[at_dict_key]["percmin"] = float(perc_array[0])  # type: ignore
                        # creo l'elemento per i giorni di caldo e lo inizializzo a zero
                        if id_venue not in giorni_di_caldo:
                            giorni_di_caldo[id_venue] = {}
                        if (
                            fine_date.strftime("%Y-%m-%d")
                            not in giorni_di_caldo[id_venue]
                        ):
                            giorni_di_caldo[id_venue][
                                fine_date.strftime("%Y-%m-%d")
                            ] = 0  # inizializzo a zero
                            # print("giorni_di_caldo", giorni_di_caldo)
                            """
                            if round(at[k], 2) != "nan":
                                if round(at[k], 2) >= float(
                                    perc_array[0]  # type:ignore
                                ):
                                    if (
                                        giorni_di_caldo[id_venue][
                                            start_date.strftime("%Y-%m-%d")
                                        ]
                                        == 0
                                    ):
                                        giorni_di_caldo[id_venue][
                                            start_date.strftime("%Y-%m-%d")
                                        ] = 1
                            """
                        start_date = start_date + datetime.timedelta(minutes=30)
                        k = k + 1

                    if parametro == "min":
                        at_min = np.nanmin(at)  # type: ignore
                        if not math.isnan(at_min):
                            at_min = round(at_min, 1)
                        else:
                            at_min = None
                        t_min = np.nanmin(terma)  # type: ignore
                        if not math.isnan(t_min):
                            t_min = round(t_min, 1)
                        else:
                            t_min = None
                        at_dict[at_dict_key]["atmin"] = at_min
                        # print("Temperatura apparente min", at_min)
                    if parametro == "max":
                        at_max = np.nanmax(at)  # type: ignore
                        if not math.isnan(at_max):
                            at_max = round(at_max, 1)
                        else:
                            at_max = None
                        t_max = np.nanmax(terma)  # type: ignore
                        if not math.isnan(t_max):
                            t_max = round(t_max, 1)
                        else:
                            t_max = None
                        at_dict[at_dict_key]["atmax"] = at_max
                        # print("Temperatura apparente max", at_max)
                    diff_from_today = (fine_date.date() - today.date()).days
                    # print("parametro - tl - diff_from_today", parametro, dayago, tl[dayago], diff_from_today)
                    if diff_from_today in tl:
                        # print("tl and ex_tl", tl[diff_from_today], ex_tl[dayago])
                        # salvo i dati
                        if parametro == "max" and tl[diff_from_today] == 48:
                            print("non salviamo", parametro, tl[diff_from_today])
                        else:
                            if parametro == "max":
                                if (
                                    HashW36Data(
                                        id_venue, tl[diff_from_today], "ATMAX", 0
                                    )
                                    in w36_data_dict
                                ):
                                    # print("---- ATMAX TL ", tl[diff_from_today])
                                    value = at_max
                                    if value is not None:
                                        value = round(at_max, 1)
                                    w36_data_dict[
                                        HashW36Data(
                                            id_venue, tl[diff_from_today], "ATMAX", 0
                                        )
                                    ].numeric_value = value
                                if (
                                    HashW36Data(
                                        id_venue, tl[diff_from_today], "TERMA", 328
                                    )
                                    in w36_data_dict
                                ):
                                    value = t_max
                                    if value is not None:
                                        value = round(t_max, 1)
                                    w36_data_dict[
                                        HashW36Data(
                                            id_venue, tl[diff_from_today], "TERMA", 328
                                        )
                                    ].numeric_value = value
                            if parametro == "min":
                                if (
                                    HashW36Data(
                                        id_venue, tl[diff_from_today], "ATMIN", 0
                                    )
                                    in w36_data_dict
                                ):
                                    # print("---- ATMIN TL ", tl[diff_from_today])
                                    value = at_min
                                    if value is not None:
                                        value = round(at_min, 1)
                                    w36_data_dict[
                                        HashW36Data(
                                            id_venue, tl[diff_from_today], "ATMIN", 0
                                        )
                                    ].numeric_value = value
                                if (
                                    HashW36Data(
                                        id_venue, tl[diff_from_today], "TERMA", 327
                                    )
                                    in w36_data_dict
                                ):
                                    value = t_min
                                    if value is not None:
                                        value = round(t_min, 1)
                                    w36_data_dict[
                                        HashW36Data(
                                            id_venue, tl[diff_from_today], "TERMA", 327
                                        )
                                    ].numeric_value = value
        # print("osservati", osservati)
        # print("at_dict", at_dict)

        def calcolaWda(
            atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile
        ):
            # print("calcolaWda", atmax_prevista, atmax_percentile, atmin_prevista, atmin_percentile)
            wda_value = 0
            # inserisco la condizione che comunque la atmax debba superare i 27°C per accendere wda
            if atmax_prevista >= 27:
                if atmax_prevista >= atmax_percentile:
                    wda_value = 1
                elif (atmax_percentile - atmax_prevista) <= 0.5:
                    if atmin_prevista >= (atmin_percentile - 0.5):
                        wda_value = 1
                    else:
                        wda_value = 0
                else:
                    wda_value = 0
            # print("calcolaWda return", wda_value)
            return wda_value

        # calcola i giorni di caldo sulla base delle at_max e at_min della giornata con calcolaWda
        for at_element in at_dict:
            id_venue = at_element.split(delimiter)[0]
            data = at_element.split(delimiter)[1]
            if "atmin" in at_dict[at_element] and "atmax" in at_dict[at_element]:
                if (
                    at_dict[at_element]["atmax"] is not None
                    and at_dict[at_element]["atmin"] is not None
                ):
                    wda = calcolaWda(
                        at_dict[at_element]["atmax"],
                        at_dict[at_element]["percmax"],
                        at_dict[at_element]["atmin"],
                        at_dict[at_element]["percmin"],
                    )
                    if giorni_di_caldo[id_venue][data] == 0:
                        giorni_di_caldo[id_venue][data] = wda
                    at_dict[at_element]["wda"] = wda
            print("at_element", id_venue, data, at_dict[at_element])
            debug = (
                debug
                + "at_element"
                + ","
                + str(id_venue)
                + ","
                + str(data)
                + ","
                + str(at_dict[at_element])
                + "\n"
            )

        # qualche test
        # giorni_di_caldo["59"]["2024-08-07"] = 1
        # giorni_di_caldo["59"]["2024-08-08"] = 1
        # giorni_di_caldo["59"]["2024-08-09"] = 1
        # giorni_di_caldo["59"]["2024-08-10"] = 0
        # giorni_di_caldo["59"]["2024-08-11"] = 1
        print("giorni_di_caldo", giorni_di_caldo)
        debug = debug + "\ngiorni_di_caldo" + "," + str(giorni_di_caldo) + "\n"
        tot_giorni_di_caldo = {}
        for id_venue in giorni_di_caldo:
            tot_giorni_di_caldo[id_venue] = 0
            # controllo a partire da ieri
            mydate = today - datetime.timedelta(days=1)
            esci = False
            if id_venue in giorni_di_caldo:
                while (
                    mydate.strftime("%Y-%m-%d") in giorni_di_caldo[id_venue]
                    and esci is False
                ):
                    if giorni_di_caldo[id_venue][mydate.strftime("%Y-%m-%d")] == 1:
                        tot_giorni_di_caldo[id_venue] = tot_giorni_di_caldo[
                            id_venue
                        ] + int(giorni_di_caldo[id_venue][mydate.strftime("%Y-%m-%d")])
                    else:
                        # al primo giorno zero cioè non di caldo esco
                        esci = True
                    mydate = mydate - datetime.timedelta(days=1)
        print("tot_giorni_di_caldo", tot_giorni_di_caldo)
        debug = debug + "\ntot_giorni_di_caldo" + "," + str(tot_giorni_di_caldo) + "\n"
        # return Response({"id_w36": new.id_w36})
        # salvo i valori previsti
        # select * from forecast_values
        #   join forecast_parameters using(id_forecast_parameter)
        #   join forecast_stations using(id_forecast_station)
        #   join forecast_runs using(id_forecast_run)
        # where date_emiss='2024-03-06' and date_rif='2024-03-06' and cod_staz_meteo='94145'
        # and time_emiss='07:35:00' and id_parametro='TERMA' and id_aggregazione=0 order by time_rif;
        # print("------- inizio lettura forecast_values")
        inizio_log = datetime.datetime.now()

        # cerco l'ultimo forecast_run di MULTMODEL che abbia tutte le stazioni cercate
        if (
            models_w35.ForecastStations.objects.select_related("id_forecast_run")
            .values(
                "id_forecast_run__date_emiss",
                "id_forecast_run__time_emiss",
                "id_forecast_run__id_forecast_run",
            )
            .filter(id_forecast_run__model_name="MULTMODEL")
            .filter(cod_staz_meteo__in=stazioni)
            .filter(id_forecast_run__date_emiss=today)
            .annotate(
                Count("id_forecast_run__date_emiss"),
                Count("id_forecast_run__time_emiss"),
                Count("id_forecast_run__id_forecast_run"),
            )
            .order_by("-id_forecast_run__date_emiss", "-id_forecast_run__time_emiss")
            .exists()
        ):
            forecast_stations = (
                models_w35.ForecastStations.objects.select_related("id_forecast_run")
                .values(
                    "id_forecast_run__date_emiss",
                    "id_forecast_run__time_emiss",
                    "id_forecast_run__id_forecast_run",
                )
                .filter(id_forecast_run__model_name="MULTMODEL")
                .filter(cod_staz_meteo__in=stazioni)
                .filter(id_forecast_run__date_emiss=today)
                .annotate(
                    Count("id_forecast_run__date_emiss"),
                    Count("id_forecast_run__time_emiss"),
                    Count("id_forecast_run__id_forecast_run"),
                )
                .order_by(
                    "-id_forecast_run__date_emiss", "-id_forecast_run__time_emiss"
                )
                .latest("id_forecast_run__id_forecast_run")
            )
            # print(forecast_stations)
            daft = today + datetime.timedelta(days=2)
            forecast_values = (
                models_w35.ForecastValues.objects.select_related(
                    "id_forecast_parameter"
                )
                .select_related("id_forecast_parameter__id_forecast_station")
                .select_related(
                    "id_forecast_parameter__id_forecast_station__id_forecast_run"
                )
                .filter(
                    id_forecast_parameter__id_parametro__in=["TERMA", "IGRO", "VELV"]
                )
                .filter(id_forecast_parameter__id_aggregazione=0)
                .filter(date_rif__gte=today, date_rif__lte=daft)
                .filter(
                    id_forecast_parameter__id_forecast_station__id_forecast_run=forecast_stations[
                        "id_forecast_run__id_forecast_run"
                    ]
                )
                .filter(
                    id_forecast_parameter__id_forecast_station__cod_staz_meteo__in=stazioni
                )
                .order_by(
                    "-id_forecast_parameter__id_forecast_station__id_forecast_run__date_emiss",
                    "-id_forecast_parameter__id_forecast_station__id_forecast_run__time_emiss",
                )
            )
            # print("forecast_values.count", len(forecast_values))
            # print("forecast_values.query", forecast_values.query)
            fv_dict = {}
            for fv in forecast_values:
                """
                print(
                    fv.id_forecast_parameter.id_forecast_station.id_forecast_run.date_emiss,
                    fv.id_forecast_parameter.id_forecast_station.id_forecast_run.time_emiss,
                    fv.id_forecast_parameter.id_forecast_station.cod_staz_meteo,
                    fv.id_forecast_parameter.id_parametro.id_parametro,
                    fv.id_forecast_parameter.id_aggregazione.id_aggregazione,
                    fv.date_rif,
                    fv.time_rif,
                    fv.value
                )
                """
                fv_dict[
                    HashFV(
                        fv.id_forecast_parameter.id_forecast_station.cod_staz_meteo,
                        fv.id_forecast_parameter.id_parametro.id_parametro,
                        fv.id_forecast_parameter.id_aggregazione.id_aggregazione,
                        fv.date_rif,
                        fv.time_rif,
                    )
                ] = fv
            tl = [48, 66, 83]  # type: ignore
            for venue in venue2stazione:
                """
                print(
                    venue,
                    venue2stazione[venue][0],
                    venue2stazione[venue][1],
                    venue2stazione[venue][2],
                )
                """

                for dayago in range(3):
                    for parametro in ["min", "max"]:
                        # print(parametro, tl[dayago])
                        if parametro == "min":
                            inizio = (
                                today + datetime.timedelta(days=dayago - 1)
                            ).replace(hour=18, minute=10)
                            # print("inizio", dayago, inizio)
                            fine = (today + datetime.timedelta(days=dayago)).replace(
                                hour=6, minute=0
                            )
                            # print("fine", dayago, fine)
                        if parametro == "max":
                            inizio = (today + datetime.timedelta(days=dayago)).replace(
                                hour=6, minute=10
                            )
                            # print("inizio", dayago, inizio)
                            fine = (today + datetime.timedelta(days=dayago)).replace(
                                hour=18, minute=0
                            )
                            # print("fine", dayago, fine)
                        inizio = inizio.timestamp()  # type: ignore
                        fine = fine.timestamp()  # type: ignore

                        terma = filterFV(
                            fv_dict,
                            12,
                            venue2stazione[venue][0],
                            "TERMA",
                            inizio,
                            fine,
                            dayago,
                        )
                        igro = filterFV(
                            fv_dict,
                            12,
                            venue2stazione[venue][1],
                            "IGRO",
                            inizio,
                            fine,
                            dayago,
                        )
                        velv = filterFV(
                            fv_dict,
                            12,
                            venue2stazione[venue][2],
                            "VELV",
                            inizio,
                            fine,
                            dayago,
                        )
                        if np.isnan(velv).all():
                            # inizializzo l'array con la velocità vento 1 m/s
                            print(
                                venue2stazione[venue][2]
                                + " VELV non ha dati setto tutto l'array con valori di 1 m/s!"
                            )
                            velv = np.full(12, 1)
                        # print("terma", dayago, terma)
                        # print("igro", dayago, igro)
                        # print("velv", dayago, velv)
                        # calcolo il max
                        if parametro == "max":
                            t_max = np.nanmax(terma)
                            i_max = np.nanargmax(terma)
                            # print("max,i_max", t_max, i_max)
                            e = (
                                6.112
                                * 10 ** ((7.5 * t_max) / (237.7 + t_max))
                                * igro[i_max]
                                / 100
                            )
                            at_max = (
                                -2.7 + 1.04 * t_max + 2 * e / 10 - 0.65 * velv[i_max]
                            )
                            if not math.isnan(at_max):
                                at_max = round(at_max, 1)
                            else:
                                at_max = None
                            # print("at_max", at_max)
                            i_igro_max = igro[i_max]
                            if math.isnan(i_igro_max):
                                i_igro_max = None
                            i_velv_max = velv[i_max]
                            if math.isnan(i_velv_max):
                                i_velv_max = None

                        if parametro == "min":
                            t_min = np.nanmin(terma)
                            i_min = np.nanargmin(terma)
                            # print("min,i_min", t_min, i_min)
                            e = (
                                6.112
                                * 10 ** ((7.5 * t_min) / (237.7 + t_min))
                                * igro[i_min]
                                / 100
                            )
                            at_min = (
                                -2.7 + 1.04 * t_min + 2 * e / 10 - 0.65 * velv[i_min]
                            )
                            if not math.isnan(at_min):
                                at_min = round(at_min, 1)
                            else:
                                at_min = None
                            # print("at_min", at_min)
                            i_igro_min = igro[i_min]
                            if math.isnan(i_igro_min):
                                i_igro_min = None
                            i_velv_min = velv[i_min]
                            if math.isnan(i_velv_min):
                                i_velv_min = None

                        if parametro == "max":
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "ATMAX", 0)
                            ].numeric_value = round(at_max, 1)
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "TERMA", 328)
                            ].numeric_value = round(t_max, 1)
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "IGRO", 328)
                            ].numeric_value = (round((i_igro_max / 10) * 2, 0) * 5)
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "VELV", 328)
                            ].numeric_value = round(i_velv_max, 0)
                        if parametro == "min":
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "ATMIN", 0)
                            ].numeric_value = round(at_min, 1)
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "TERMA", 327)
                            ].numeric_value = round(t_min, 1)
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "IGRO", 327)
                            ].numeric_value = (round((i_igro_min / 10) * 2, 0) * 5)
                            w36_data_dict[
                                HashW36Data(venue, tl[dayago], "VELV", 327)
                            ].numeric_value = round(i_velv_min, 0)

                    # creazione record impostati a 0 per il codice_colore previsto
                    # sono valorizzati a livello di frontend
                    w36_data_dict[
                        HashW36Data(venue, tl[dayago], "COD_COLORE", 0)
                    ].numeric_value = 0
                    w36_data_dict[
                        HashW36Data(venue, tl[dayago], "COD_COLORE_ORIG", 0)
                    ].numeric_value = 0
            fine_log = datetime.datetime.now()
            print(
                "lettura forecast_value finito in ",
                abs((fine_log - inizio_log).total_seconds()),
                "secondi",
            )

        # PERCENTILI GIORNI OSSERVATI E PREVISTI
        # lettura percentili da w36_percentili per i 3 giorni di previsione e i 2 gg precedenti
        mesi = []
        giorni = []
        mmgg = []
        data2tl = {"-2": 15, "-1": 32, "0": 48, "1": 66, "2": 83}
        # valorizzo l'array solo con i giorni di interesse, utile per filtrare i dati del queryset
        for day in range(-2, 3):
            giorno = today + datetime.timedelta(days=day)
            mmgg.append(str(giorno.month) + "_" + str(giorno.day))
            giorni.append(str(giorno.day))
            mesi.append(str(giorno.month))

        w36_percentili = (
            models.W36Percentili.objects.filter(mese__in=mesi)
            .filter(giorno__in=giorni)
            .order_by("id_venue", "mese", "giorno")
        )
        # ciclo sul queryset e creo i record su w36_data per i 3 gg di previsione
        for w36p in w36_percentili:
            mmgg_perc = str(w36p.mese) + "_" + str(w36p.giorno)
            # solo per i giorni d'interesse (2 osservati e 3 previsti)
            if mmgg_perc in mmgg:
                # creo la data relativa al pecentile
                dateperc = datetime.datetime(today.year, w36p.mese, w36p.giorno)
                days_diff = dateperc.date() - today.date()
                # salvo su db i percentili per ATMAX e ATMIN 3 gg previsionali
                w36_data_dict[
                    HashW36Data(
                        w36p.id_venue.id_venue,
                        data2tl[str(days_diff.days)],
                        w36p.id_parametro.id_parametro,
                        w36p.id_aggregazione.id_aggregazione,
                    )
                ].numeric_value = w36p.numeric_value

        # GIORNI CONSECUTIVI DI CALDO
        # Per prima cosa verifico se è il primo bollettino della stagione:
        yesterday = today - datetime.timedelta(days=1)
        gg_cons_altroieri = []  # type: ignore
        old_w36_data_queryset = models.W36.objects.filter(
            data_emissione=yesterday.date()
        ).filter(status="1")

        # se esiste boll di ieri leggo per ogni venue i gg consecutivi dell'altroieri (tl=15)
        if old_w36_data_queryset.exists():
            yesterday_w36 = old_w36_data_queryset.get()
            yesterday_id = yesterday_w36.id_w36
            # print("ricavo i giorni cosecutivi di caldo")
            gg_cons_altroieri = (
                models.W36Data.objects.values("id_venue", "numeric_value")  # type: ignore
                .filter(id_w36=yesterday_id)
                .filter(id_parametro="GGCONS")
                .filter(id_time_layouts=15)
                .order_by("id_venue")
            )
            # print("ho trovato il bollettino di ieri gg_cons_altroieri", gg_cons_altroieri)
        # se non esiste imposto a 0 i giorni consecutivi di caldo dell'altroieri
        else:
            print("Primo bollettino della stagione. Imposto a 0 i giorni cons di caldo")
            for venue in venue2stazione:
                x = {"id_venue": venue, "numeric_value": 0.0}
                gg_cons_altroieri.append(x)
            # print("NON ho trovato il bollettino di ieri gg_cons_altroieri", gg_cons_altroieri)

        gg_cons_altroieri_orig = gg_cons_altroieri

        # WDA E CODICE COLORE DI IERI
        # Creazione dei record per i codici colore di ieri: ciclo per ogni venue, calcolo i 3 wda
        # e trovo il codice colore tenendo conto di gg_cons_altroieri (perché non posso uscire in
        # rosso se il sistema non è acceso da 3 giorni)

        def calcolaCodiceColore(wda75p, wda90p, wda95p, ggcons_ggprec):
            codice_colore = 0
            # il codice è rosso solo se era caldo sia 2 sia 3 giorni fa
            if wda95p == 1:
                if ggcons_ggprec == 2:
                    codice_colore = 3
                else:
                    codice_colore = 2
            elif wda90p == 1:
                codice_colore = 2
            elif wda75p == 1:
                codice_colore = 1

            return codice_colore

        # ciclo per ogni venue, estraggo i param per il calcolo dei 3 wda di ieri
        for venue in venue2stazione:
            # print("inizio venue", venue)
            for dict in gg_cons_altroieri:
                if dict["id_venue"] == venue:
                    ggcons_altroieri_venue = dict["numeric_value"]
            for dict_orig in gg_cons_altroieri_orig:
                if dict_orig["id_venue"] == venue:
                    ggcons_altroieri_orig_venue = dict_orig["numeric_value"]
            wda = []
            atmax_ieri = w36_data_dict[HashW36Data(venue, 32, "ATMAX", 0)].numeric_value
            atmin_ieri = w36_data_dict[HashW36Data(venue, 32, "ATMIN", 0)].numeric_value
            if atmax_ieri is not None and atmin_ieri is not None:
                # wda è un array fatto così [wda75p, wda90p, wda95p]
                for aggreg in [940, 941, 942]:
                    atmax_percentile = w36_data_dict[
                        HashW36Data(venue, 32, "ATMAX", aggreg)
                    ].numeric_value
                    atmin_percentile = w36_data_dict[
                        HashW36Data(venue, 32, "ATMIN", aggreg)
                    ].numeric_value
                    wda.append(
                        calcolaWda(
                            atmax_ieri, atmax_percentile, atmin_ieri, atmin_percentile
                        )
                    )
                codice_colore = calcolaCodiceColore(
                    wda[0], wda[1], wda[2], ggcons_altroieri_venue
                )
            else:
                codice_colore = None

            # print("codice_colore", venue, wda, codice_colore)

            w36_data_dict[HashW36Data(venue, 32, "COD_COLORE", 0)].numeric_value = (
                codice_colore
            )
            w36_data_dict[
                HashW36Data(venue, 32, "COD_COLORE_ORIG", 0)
            ].numeric_value = codice_colore

            # se il wda di ieri si accende => incremento i gg consecutivi e salvo su db
            # print("wda", venue, wda)
            """
            if wda:  # not empty
                if wda[0] == 1:
                    ggcons_ieri_venue = ggcons_altroieri_venue + 1
                # altrimenti azzero il contatore
                else:
                    ggcons_ieri_venue = 0
            else:
                ggcons_ieri_venue = None
            print("ggcons", venue, ggcons_ieri_venue, ggcons_altroieri_venue)
            w36_data_dict[
                HashW36Data(venue, 32, "GGCONS", 0)
            ].numeric_value = ggcons_ieri_venue
            w36_data_dict[
                HashW36Data(venue, 15, "GGCONS", 0)
            ].numeric_value = ggcons_altroieri_venue
            """
            if str(venue) in tot_giorni_di_caldo:
                if tot_giorni_di_caldo[str(venue)] >= (my_days_ago - 1):
                    # in questo caso non sono più in grado di capire quando è iniziato il caldo
                    # prendo i dati salvati su db perchè adesso la catena di calcolo
                    # dovrebbe essere corretta in quanto sono partito dai dati osservati
                    w36_data_dict[HashW36Data(venue, 32, "GGCONS", 0)].numeric_value = (
                        ggcons_altroieri_orig_venue + 2
                    )
                    w36_data_dict[HashW36Data(venue, 15, "GGCONS", 0)].numeric_value = (
                        ggcons_altroieri_orig_venue + 1
                    )
                else:
                    # prendo il wda derivato dai dati osservati
                    w36_data_dict[HashW36Data(venue, 32, "GGCONS", 0)].numeric_value = (
                        tot_giorni_di_caldo[str(venue)]
                    )
                    if tot_giorni_di_caldo[str(venue)] - 1 < 0:
                        w36_data_dict[
                            HashW36Data(venue, 15, "GGCONS", 0)
                        ].numeric_value = tot_giorni_di_caldo[str(venue)]
                    else:
                        w36_data_dict[
                            HashW36Data(venue, 15, "GGCONS", 0)
                        ].numeric_value = (tot_giorni_di_caldo[str(venue)] - 1)
            else:
                # in questo caso non saprei che fare e quindi
                # prendo i dati salvati su db
                w36_data_dict[HashW36Data(venue, 32, "GGCONS", 0)].numeric_value = (
                    ggcons_altroieri_orig_venue + 2
                )
                w36_data_dict[HashW36Data(venue, 15, "GGCONS", 0)].numeric_value = (
                    ggcons_altroieri_orig_venue + 1
                )
            # print("fine venue", venue)
            # print("")

        # dati per la parte sanitaria, attesi e codice_salute, solo per torino

        # lettura attesi da w36_decessi_attesi per i 3 giorni di previsione
        today = datetime.datetime.today()
        tomorrow = today + datetime.timedelta(days=1)
        dayaftertomorrow = today + datetime.timedelta(days=2)

        # seleziono solo i 3 giorni relativi al bollettino, filtro quindi su mese e giorno
        w36_attesi = models.W36DecessiAttesi.objects.filter(
            mese__in=[today.month, tomorrow.month, dayaftertomorrow.month]
        ).filter(giorno__in=[today.day, tomorrow.day, dayaftertomorrow.day])
        # ciclo sul queryset e creo i record su w36_data per i 3 gg di previsione
        for w36a in w36_attesi:
            tl = -1  # type: ignore
            if w36a.mese == today.month and w36a.giorno == today.day:
                tl = 48  # type: ignore
            elif w36a.mese == tomorrow.month and w36a.giorno == tomorrow.day:
                tl = 66  # type: ignore
            elif (
                w36a.mese == dayaftertomorrow.month
                and w36a.giorno == dayaftertomorrow.day
            ):
                tl = 83  # type: ignore
            if tl > 0:  # type: ignore
                w36_data_dict[
                    HashW36Data(w36a.id_venue.id_venue, tl, "ATTESI", 0)
                ].numeric_value = w36a.numeric_value
            # -----------------------------

        venue = 59
        for tl in [48, 66, 83]:  # type: ignore
            # w36_data_dict[HashW36Data(venue, tl, "ATTESI", 0)].numeric_value = None
            w36_data_dict[HashW36Data(venue, tl, "COD_SALUTE", 0)].numeric_value = None

        # salvataggio di tutti i record con bulk_create
        w36_json["w36data_set"] = []  # type: ignore
        w36_data_list = []
        for w36_data in w36_data_dict:
            w36_data_list.append(w36_data_dict[w36_data])
            tmp = {}
            tmp["numeric_value"] = w36_data_dict[w36_data].numeric_value
            tmp["id_w36"] = w36_data_dict[w36_data].id_w36.id_w36
            tmp["id_venue"] = w36_data_dict[w36_data].id_venue.id_venue
            tmp["id_time_layouts"] = w36_data_dict[
                w36_data
            ].id_time_layouts.id_time_layouts
            tmp["id_parametro"] = w36_data_dict[w36_data].id_parametro.id_parametro  # type: ignore
            tmp["id_aggregazione"] = w36_data_dict[
                w36_data
            ].id_aggregazione.id_aggregazione
            w36_json["w36data_set"].append(OrderedDict(tmp))  # type: ignore
        models.W36Data.objects.bulk_create(w36_data_list)

        w36 = models.W36.objects.get(id_w36=new.id_w36)
        w36.chart_max = plotchart(w36_json, 328)
        w36.chart_min = plotchart(w36_json, 327)
        w36.osservati = osservati
        w36.debug = debug
        w36.save()

        return Response({"id_w36": new.id_w36})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W36.objects.get(pk=pk)
        print("w36 reopen:", old)
        old.status = "2"
        old_id_w36 = old.id_w36
        old.save()

        new = old
        # aumento il sequenziale perchè è una nuova emissione
        new.seq_num = int(old.seq_num)  # type: ignore
        new.seq_num = new.seq_num + 1
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w36_parent = old_id_w36
        new.save()
        # print('created: ', new)
        old_data = models.W36Data.objects.filter(id_w36=old_id_w36)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w36 = new
            new_data.save()

        return Response({"id_w36": new.id_w36})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== INIZIO")
        print("========== POST /w36/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        print("========== FINE")
        print("==========")
        updated = 0
        snapshots = self.request.data
        torino_venue = False

        id_w36 = next(s["id"] for s in snapshots if s["id_key"] == "id_w36")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w36",
            "id": id_w36,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w36 = models.W36.objects.get(pk=id_w36)
        fields = {}  # type: ignore
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w36":
                """
                print(
                    "id_w36:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                )
                """
                setattr(w36, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                w36_data = models.W36Data.objects.get(pk=snapshot["id"])
                if w36_data.id_venue.id_venue == 59:
                    torino_venue = True
                print(
                    "id_w36_data:",
                    snapshot["id"],
                    snapshot["value_key"],
                    snapshot["new_value"],
                    w36_data.id_parametro.id_parametro,
                )
                setattr(w36_data, snapshot["value_key"], snapshot["new_value"])
                # w36_data.save()
                if snapshot["value_key"] not in fields:
                    fields[snapshot["value_key"]] = []
                fields[snapshot["value_key"]].append(w36_data)
                updated += 1
        if len(fields) > 0:
            for field in fields:
                print("aggiorno", field, fields[field])
                my_field = []
                my_field.append(field)
                models.W36Data.objects.bulk_update(fields[field], my_field)
        w36.save()
        fine = datetime.datetime.now()
        serializer = W36SerializerFull(w36, context={"request": request})
        if torino_venue:
            print("la venue è torino rigenero il grafico")
            mpa = serializer.data
            w36.chart_max = plotchart(mpa, 328)
            w36.chart_min = plotchart(mpa, 327)
            w36.save()
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


class W36DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W36 bulletin Data to be viewed or edited
    """

    queryset = models.W36Data.objects.all().order_by("id_w36_data")
    serializer_class = W36DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W36Data.objects
        w36Data = get_object_or_404(queryset, pk=pk)
        serializer = W36DataSerializer(w36Data, context={"request": request})
        return Response(serializer.data)


def plotchart(mpa, aggreg):
    # funzione per la creazione del grafico
    days = []
    temperature = []
    app_temperature = []
    values_temp = []
    values_app_temp = []
    labels = []
    tl_max_sorted = (301, 300, 15, 32, 48, 66, 83)

    # print("SONO NELLA GENERAZIONE DEL GRAFICO" + str(aggreg))
    today = datetime.datetime.strptime(mpa["data_emissione"], "%Y-%m-%d")
    tomorrow = today + datetime.timedelta(days=1)
    dayaftertomorrow = today + datetime.timedelta(days=2)
    yesterday = today - datetime.timedelta(days=1)
    twodaybeforyes = today - datetime.timedelta(days=2)
    threedaybeforyes = today - datetime.timedelta(days=3)
    fourdaybeforyes = today - datetime.timedelta(days=4)
    date_grafico = {
        301: str(fourdaybeforyes.day).rjust(2, "0")
        + "/"
        + str(fourdaybeforyes.month).rjust(2, "0"),
        300: str(threedaybeforyes.day).rjust(2, "0")
        + "/"
        + str(threedaybeforyes.month).rjust(2, "0"),
        15: str(twodaybeforyes.day).rjust(2, "0")
        + "/"
        + str(twodaybeforyes.month).rjust(2, "0"),
        32: str(yesterday.day).rjust(2, "0") + "/" + str(yesterday.month).rjust(2, "0"),
        48: str(today.day).rjust(2, "0") + "/" + str(today.month).rjust(2, "0"),
        66: str(tomorrow.day).rjust(2, "0") + "/" + str(tomorrow.month).rjust(2, "0"),
        83: str(dayaftertomorrow.day).rjust(2, "0")
        + "/"
        + str(dayaftertomorrow.month).rjust(2, "0"),
    }

    if aggreg == 328:
        parametro = "ATMAX"
        stringa = "massima"
        colore_t = "orange"
        colore_at = "red"
    elif aggreg == 327:
        parametro = "ATMIN"
        stringa = "minima"
        colore_t = "royalblue"
        colore_at = "mediumturquoise"

    for test in mpa["w36data_set"]:
        if (
            str(test["id_venue"]) == "59"
            and test["id_parametro"] == "TERMA"
            and str(test["id_aggregazione"]) == str(aggreg)
        ):
            values_temp.append((test["id_time_layouts"], test["numeric_value"]))

        # Ricavo i 3 valori previsionali con tl 48, 66, 83 ['301', '300', '15', '32'] e aggreg =0
        if (
            str(test["id_venue"]) == "59"
            and test["id_parametro"] == parametro
            and str(test["id_aggregazione"]) == "0"
        ):
            values_app_temp.append((test["id_time_layouts"], test["numeric_value"]))

    # i tl non sono crescenti, devo ordinarli secondo la sequenza in tl_max_sorted
    for tl_s in tl_max_sorted:
        for e in values_temp:
            if e[0] == tl_s:
                if e[1] is not None:
                    temperature.append(round(e[1]))
                else:
                    temperature.append(e[1])

        for e in values_app_temp:
            if e[0] == tl_s:
                if e[1] is not None:
                    app_temperature.append(round(e[1]))
                else:
                    app_temperature.append(e[1])
                days.append(tl_max_sorted.index(e[0]))
                labels.append(date_grafico[e[0]])

    plt.clf()
    try:
        plt.ylim(
            [
                min(x for x in temperature + app_temperature if x is not None) - 1,
                max(x for x in temperature + app_temperature if x is not None) + 1,
            ]
        )
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        plt.ylim(
            [
                -40,
                40,
            ]
        )
    plt.rcParams.update({"font.size": 14})
    plt.plot(
        days,
        temperature,
        marker="o",
        linewidth=2,
        color=colore_t,
        label="T. " + stringa,
    )
    plt.plot(
        days,
        app_temperature,
        marker="o",
        linewidth=2,
        color=colore_at,
        label="T. " + stringa + " percepita",
    )
    for a, b in zip(days, app_temperature):
        if a is not None and b is not None:
            plt.text(
                a - 0.1,
                b + 0.2,
                str(b),
                bbox=dict(
                    facecolor="white",
                    alpha=0.9,
                    boxstyle="round,pad=0.01",
                    edgecolor="white",
                ),
            )
    for a, b in zip(days, temperature):
        if a is not None and b is not None:
            plt.text(
                a - 0.1,
                b + 0.2,
                str(b),
                bbox=dict(
                    facecolor="white",
                    alpha=0.9,
                    boxstyle="round,pad=0.01",
                    edgecolor="white",
                ),
            )
    plt.legend()
    plt.xticks(days, labels)
    plt.axvline(x=4, linestyle="dotted")
    plt.show()
    plt.xlabel("data", fontsize=18)
    plt.ylabel("T (°C)", fontsize=18)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return image_png


def convert_to_date(d, k):
    # TODO when support for Postgres 9.3 is dropped, remove the `replace` function call
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


def caldo_rearranged_func(caldo):
    caldo_rearranged = {}  # type: ignore
    for data in caldo["w36data_set"]:
        if data["id_parametro"] not in caldo_rearranged:
            caldo_rearranged[data["id_parametro"]] = {}
        if data["id_time_layouts"] not in caldo_rearranged[data["id_parametro"]]:
            caldo_rearranged[data["id_parametro"]][data["id_time_layouts"]] = {}
        if (
            data["id_venue"]
            not in caldo_rearranged[data["id_parametro"]][data["id_time_layouts"]]
        ):
            caldo_rearranged[data["id_parametro"]][data["id_time_layouts"]][
                data["id_venue"]
            ] = {}
        if (
            data["id_aggregazione"]
            not in caldo_rearranged[data["id_parametro"]][data["id_time_layouts"]][
                data["id_venue"]
            ]
        ):
            caldo_rearranged[data["id_parametro"]][data["id_time_layouts"]][
                data["id_venue"]
            ][data["id_aggregazione"]] = {}
        if data["numeric_value"] is None:
            caldo_rearranged[data["id_parametro"]][data["id_time_layouts"]][
                data["id_venue"]
            ][data["id_aggregazione"]] = data["numeric_value"]
        else:
            caldo_rearranged[data["id_parametro"]][data["id_time_layouts"]][
                data["id_venue"]
            ][data["id_aggregazione"]] = int(round(data["numeric_value"], 0))

    return caldo_rearranged


class CaldoTorinoHTMLView(TemplateView):
    template_name = "caldo_torino.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W36.objects
        w36 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W36SerializerFull(w36)
        caldo = serializer.data

        caldo_rearranged = {}
        caldo_rearranged = caldo_rearranged_func(caldo)

        graphic_max = caldo["chart_max"]
        graphic_min = caldo["chart_min"]

        convert_to_date(caldo, "data_emissione")

        context = {
            "caldo": caldo,
            "caldo_rearranged": caldo_rearranged,
            "graphic_min": graphic_min,
            "graphic_max": graphic_max,
            "title": "Bollettino caldo Torino",
        }
        return context


class CaldoRegioneHTMLView(TemplateView):
    template_name = "caldo_regione.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W36.objects
        w36 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W36SerializerFull(w36)
        caldo = serializer.data

        caldo_rearranged = {}
        caldo_rearranged = caldo_rearranged_func(caldo)

        convert_to_date(caldo, "data_emissione")

        context = {
            "caldo": caldo,
            "caldo_rearranged": caldo_rearranged,
            "title": "Bollettino caldo Regione",
        }
        return context


class CaldoTorinoPDFView(CaldoTorinoHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="caldo_torino.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class CaldoRegionePDFView(CaldoRegioneHTMLView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="caldo_regione.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class KmlView(TemplateView):
    template_name = "caldo_regione.kml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        today = datetime.datetime.today()
        queryset = models.W36.objects
        w36 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W36SerializerFull(w36)
        caldo = serializer.data
        oggi = "no"
        if datetime.datetime.strptime(
            str(caldo["data_emissione"]), "%Y-%m-%d"
        ).strftime("%Y-%m-%d") == today.strftime("%Y-%m-%d"):
            oggi = "si"

        caldo_rearranged = {}
        caldo_rearranged = caldo_rearranged_func(caldo)

        convert_to_date(caldo, "data_emissione")

        context = {
            "caldo": caldo,
            "caldo_rearranged": caldo_rearranged,
            "title": "Bollettino caldo Regione",
            "oggi": oggi,
        }
        return context


class W36CurrentView(RetrieveAPIView):
    """
    API endpoint that allows W36 bulletin Data to be viewed or edited
    """

    queryset = models.W36.objects.filter(status="1").order_by("-last_update")
    serializer_class = W36SerializerFull
    lookup_field = "data_emissione"
    lookup_url_kwarg = "emissione"

    def get_object(self):
        count = (
            models.W36.objects.filter(data_emissione=self.kwargs["emissione"])
            .filter(status="1")
            .order_by("-last_update")
            .count()
        )
        print(count)
        if count >= 0 and count < 2:
            queryset = self.filter_queryset(self.get_queryset())
            obj = get_object_or_404(queryset, data_emissione=self.kwargs["emissione"])
        else:
            obj = models.W36.objects.filter(
                data_emissione=self.kwargs["emissione"]
            ).order_by("-last_update")[0]
        self.check_object_permissions(self.request, obj)
        return obj
