#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
import locale
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

from w15.back import models
from w15.back.serializers import W15DataSerializer, W15Serializer, W15SerializerFull
from w35.back import models as models_w35
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core import models as models_w05

delimiter = "__"


def HashW15Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
    return (
        str(id_venue)
        + delimiter
        + id_parametro
        + delimiter
        + str(id_aggregazione)
        + delimiter
        + str(id_time_layouts)
    )


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W15View(viewsets.ModelViewSet):
    """
    API endpoint that allows W15 bulletins to be viewed or edited
    """

    queryset = models.W15.objects.order_by("-last_update", "-pk")
    serializer_class = W15Serializer
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
        queryset = models.W15.objects
        if (
            instance.id_w15_parent
            and queryset.filter(pk=instance.id_w15_parent).exists()
        ):
            w15 = get_object_or_404(queryset, pk=instance.id_w15_parent)
            w15.status = "1"
            if not User.objects.filter(username=w15.username).exists():
                print("perform_destroy non trovo l'utente " + w15.username)
                w15.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w15.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W15.objects
        w15 = get_object_or_404(queryset, pk=pk)
        serializer = W15SerializerFull(w15, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        def trend(now, old):
            # 0 | Stazionario
            # 1 | In Aumento
            # 2 | In Diminuzione
            if now is None or old is None:
                return None
            if now < old:
                return 2
            elif now == old:
                return 0
            else:
                return 1

        today = datetime.datetime.today()
        inizio = datetime.datetime.now()
        w15 = models.W15.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w15.id_w15,
            "del",
            w15.data_emissione,
            "iniziato",
        )
        w15.status = "1"
        w15.username = request.user.username
        w15.last_update = inizio
        w15.save()
        # ricalcolo i trend e li salvo
        w15_data_dict = {}
        w15_datas = models.W15Data.objects.filter(id_w15=w15.id_w15)
        for w15_data in w15_datas:
            w15_data_dict[
                HashW15Data(
                    w15_data.id_venue.id_venue,
                    w15_data.id_parametro.id_parametro,
                    w15_data.id_aggregazione.id_aggregazione,
                    w15_data.id_time_layouts.id_time_layouts,
                )
            ] = w15_data

        for w15_data_hash in w15_data_dict:
            w15_data = w15_data_dict[w15_data_hash]
            if w15_data.id_parametro.id_parametro == "TERMA":
                if w15_data.id_time_layouts.id_time_layouts == 65:
                    w15_hash_array = w15_data_hash.split(delimiter)
                    w15_hash_array[3] = str(48)
                    w15_data_old = w15_data_dict[delimiter.join(w15_hash_array)]
                    w15_data.id_trend = trend(
                        w15_data.numeric_value,
                        w15_data_old.numeric_value,
                    )
                if w15_data.id_time_layouts.id_time_layouts == 82:
                    w15_hash_array = w15_data_hash.split(delimiter)
                    w15_hash_array[3] = str(65)
                    w15_data_old = w15_data_dict[delimiter.join(w15_hash_array)]
                    w15_data.id_trend = trend(
                        w15_data.numeric_value,
                        w15_data_old.numeric_value,
                    )
                if w15_data.id_time_layouts.id_time_layouts == 48:
                    w15_hash_array = w15_data_hash.split(delimiter)
                    w15_hash_array[3] = str(33)
                    w15_data_old = w15_data_dict[delimiter.join(w15_hash_array)]
                    w15_data.id_trend = trend(
                        w15_data.numeric_value,
                        w15_data_old.numeric_value,
                    )
                if w15_data.id_time_layouts.id_time_layouts == 81:
                    w15_hash_array = w15_data_hash.split(delimiter)
                    w15_hash_array[3] = str(64)
                    w15_data_old = w15_data_dict[delimiter.join(w15_hash_array)]
                    w15_data.id_trend = trend(
                        w15_data.numeric_value,
                        w15_data_old.numeric_value,
                    )
                if w15_data.id_time_layouts.id_time_layouts == 64:
                    w15_hash_array = w15_data_hash.split(delimiter)
                    w15_hash_array[3] = str(51)
                    w15_data_old = w15_data_dict[delimiter.join(w15_hash_array)]
                    w15_data.id_trend = trend(
                        w15_data.numeric_value,
                        w15_data_old.numeric_value,
                    )

        # salvo i w15_data con i trend corretti
        w15_data_list = []
        for w15_data in w15_data_dict:
            w15_data_list.append(w15_data_dict[w15_data])
        models.W15Data.objects.bulk_update(w15_data_list, ["id_trend"])

        # salva su forecast_comuni se possibile (se è già stato fatto in data odierna)
        if (
            models_w35.ForecastComuni.objects.filter(
                id_comune__in=[63, 272, 164, 51, 171, 292]
            )
            .filter(data_emissione=today)
            .exists()
        ):
            id_comune_to_id_venue = {
                63: [55],  # Caselle Torinese MET-14
                272: [59],  # Torino MET-14
                164: [157],  # Nichelino MET-15
                51: [158],  # Candiolo MET-15
                171: [159],  # Orbassano MET-15
                292: [165],  # Venaria Reale MET-14
            }
            wind_class_dict = {}
            wind_classes = models_w35.WindClass.objects.all()
            for wind_class in wind_classes:
                wind_class_dict[wind_class.code] = wind_class

            # salvo i w15_data in forecast_comuni
            for fc in models_w35.ForecastComuni.objects.filter(
                id_comune__in=[63, 272, 164, 51, 171, 292]
            ).filter(data_emissione=today):
                # print(
                #    "w15 send: trovo dei record di oggi su forecast_comuni provo ad aggiornarli",
                #    fc,
                # )
                for w15_data_hash in w15_data_dict:
                    w15_data = w15_data_dict[w15_data_hash]
                    if w15_data.id_time_layouts == fc.id_time_layouts:
                        if (
                            w15_data.id_venue.id_venue
                            in id_comune_to_id_venue[fc.id_comune.id_comune]
                        ):
                            # print(
                            #    "w15 send: trovo il corrispettivo record su w15_data",
                            #    w15_data,
                            #    w15_data.id_venue.id_venue,
                            #    w15_data.id_parametro.id_parametro,
                            #    w15_data.id_time_layouts.id_time_layouts,
                            # )
                            if w15_data.id_parametro.id_parametro == "TERMA":
                                # print("w15 send: modifico TERMA")
                                fc.air_temperature = w15_data.numeric_value
                                fc.trend = (
                                    w15_data.id_trend
                                )  # non c'è la foreign key con id_trend e inoltre su forecast_comuni non ci sono trend salvati  # noqa: E501
                            elif w15_data.id_parametro.id_parametro == "WIND_CLASS":
                                # print("w15 send: modifico WIND_CLASS")
                                fc.wind_class = wind_class_dict[w15_data.numeric_value]  # type: ignore
                            else:
                                print(
                                    "w15 send: errore non trovo il parametro",
                                    w15_data.id_parametro,
                                )
                            # print("------------------------------------")
                fc.last_update = inizio
                fc.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("previsioni_parchi_reali", w15.id_w15)
        return Response({"id_w15": w15.id_w15})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        def my_max(one, two):
            if one is None and two is None:
                return None
            if one is not None and two is None:
                return one
            if one is None and two is not None:
                return two
            return max(one, two)

        map_terma_id_time_layout = {
            50: 48,
            67: 65,
            68: 64,
            84: 82,
            85: 81,
            33: 33,
            51: 51,
        }

        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today

        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        # tomorrow = emissione + datetime.timedelta(days=1)
        # today_bulletins = models.W15.objects.filter(data_emissione=today.date()).count()
        # if today_bulletins >= 1:
        #     raise ExistingTodayBulletin()
        old_w15 = None
        if (
            models.W15.objects.filter(status="1")
            .filter(data_emissione__year=today.year)
            .order_by("-last_update")
            .exists()
        ):
            old_w15 = (
                models.W15.objects.filter(status="1")
                .filter(data_emissione__year=today.year)
                .order_by("-last_update")
                .latest("pk")
            )
        if old_w15 is not None:
            print(
                "new del bollettino ",
                old_w15.id_w15,
                "del",
                old_w15.data_emissione,
                "iniziato",
            )
            # aumento il sequenziale perchè è una nuova emissione
            seq_num = int(old_w15.seq_num)  # type: ignore
            seq_num = seq_num + 1
        else:
            seq_num = 1

        print("old_w15", old_w15)
        new = models.W15(
            data_emissione=emissione.date(),
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            seq_num=seq_num,
        )
        new.save()

        venue = models_w05.Venue.objects.all()
        venue_dict = {}
        for m in venue:
            venue_dict[m.id_venue] = m

        time_layouts = models_w05.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for t in time_layouts:
            time_layouts_dict[t.id_time_layouts] = t

        aggregazione = models_w05.Aggregazione.objects.all().order_by("id_aggregazione")
        aggregazione_dict = {}
        for a in aggregazione:
            aggregazione_dict[a.id_aggregazione] = a

        parametri = models_w05.Parametro.objects.all()
        parametri_dict = {}
        for p in parametri:
            parametri_dict[p.id_parametro] = p

        wind_class_dict = {}
        wind_classes = models_w35.WindClass.objects.all()
        for wind_class in wind_classes:
            wind_class_dict[wind_class.code] = wind_class

        # carico la configurazione json per sapere quanti record ci devono essere su w15_data
        with open("config/w15_data.json") as json_file:
            w15_data_config = json.load(json_file)

        # creo tutti i w15_data con valori nulli
        w15_data_new_dict = {}
        for w15 in w15_data_config:
            w15_data_new_dict[
                HashW15Data(
                    w15["id_venue"],
                    w15["id_parametro"],
                    w15["id_aggregazione"],
                    w15["id_time_layouts"],
                )
            ] = models.W15Data(  # type: ignore
                id_w15=new,
                id_venue=venue_dict[w15["id_venue"]],
                id_parametro=parametri_dict[w15["id_parametro"]],
                id_aggregazione=aggregazione_dict[w15["id_aggregazione"]],
                id_time_layouts=time_layouts_dict[w15["id_time_layouts"]],
                numeric_value=None,
                id_trend=None,
            )

        # prendo i dati da weather_values tranne i TERMA perchè i TERMA hanno id_time_layouts vecchi
        weather_values_not_terma = (
            models_w05.WeatherValues.objects.all()
            .select_related(
                "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
            )
            .filter(id_venue__in=[55, 59, 157, 158, 159, 165, 166, 170])
            .filter(id_time_layouts__in=[48, 64, 65, 66, 81, 82, 83])
            .exclude(id_parametro="TERMA")
        )
        weather_values_dict = {}
        for w in weather_values_not_terma:
            weather_values_dict[
                HashW15Data(
                    w.id_venue.id_venue,
                    w.id_parametro.id_parametro,
                    w.id_aggregazione.id_aggregazione,
                    w.id_time_layouts.id_time_layouts,
                )
            ] = w

        # prendo i dati da weather_values solo i TERMA con i time_layouts vecchi
        weather_values_terma = (
            models_w05.WeatherValues.objects.all()
            .select_related(
                "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
            )
            .filter(id_venue__in=[55, 59, 157, 158, 159, 165, 166, 170])
            .filter(id_time_layouts__in=[50, 67, 68, 84, 85, 33, 61])
            .filter(id_parametro="TERMA")
        )
        for w in weather_values_terma:
            id_time_layouts = map_terma_id_time_layout[
                w.id_time_layouts.id_time_layouts
            ]
            weather_values_dict[
                HashW15Data(
                    w.id_venue.id_venue,
                    w.id_parametro.id_parametro,
                    w.id_aggregazione.id_aggregazione,
                    id_time_layouts,
                )
            ] = w

        for w15 in w15_data_new_dict:
            if w15 in weather_values_dict:
                if weather_values_dict[w15].original_numeric_values is not None:
                    w15_data_new_dict[w15].numeric_value = weather_values_dict[
                        w15
                    ].original_numeric_values  # type: ignore

                if weather_values_dict[w15].original_trend is not None:
                    w15_data_new_dict[w15].id_trend = weather_values_dict[
                        w15
                    ].original_trend.id_trend  # type: ignore

        # se c'è il forecast_comuni aggiornato prendo i dati dal forecast_comuni
        if (
            models_w35.ForecastComuni.objects.filter(
                id_comune__in=[63, 272, 164, 51, 171, 292]
            )
            .filter(data_emissione=today)
            .exists()
        ):
            print("w15 new: prendo previsioni da forecast_comuni")

            id_venue_to_id_comune = {
                55: 63,  # Caselle Torinese MET-14
                59: 272,  # Torino MET-14
                157: 164,  # Nichelino MET-15
                158: 51,  # Candiolo MET-15
                159: 171,  # Orbassano MET-15
                165: 292,  # Venaria Reale MET-14
                166: 171,  # Parco naturale di Stupinigi (eredita l'icona di MET-15 da Orbassano)
                170: 292,  # Parco naturale La Mandria (eredita l'icona di MET-14 da Venaria)
            }
            # popolo il dizionario per i forecast_comuni di oggi
            forecast_comuni_dict = {}
            for fc in models_w35.ForecastComuni.objects.filter(
                id_comune__in=[63, 272, 164, 51, 171, 292]
            ).filter(data_emissione=today):
                forecast_comuni_dict[
                    str(fc.id_comune.id_comune)
                    + delimiter
                    + str(fc.id_time_layouts.id_time_layouts)
                ] = fc

            # aggiungo il massimo della classe di vento per id_time_layouts 66 e 83 che il w15_data ha!
            for id_comune in [63, 272, 164, 51, 171, 292]:
                fc_64 = forecast_comuni_dict[str(id_comune) + delimiter + str(64)]
                wind_class_66 = wind_class_dict[
                    my_max(
                        forecast_comuni_dict[
                            str(id_comune) + delimiter + str(64)
                        ].wind_class.code,  # type: ignore
                        forecast_comuni_dict[
                            str(id_comune) + delimiter + str(65)
                        ].wind_class.code,  # type: ignore
                    )
                ]
                fc = models_w35.ForecastComuni(
                    id_comune=fc_64.id_comune,
                    id_time_layouts=time_layouts_dict[66],
                    wind_class=wind_class_66,
                )
                forecast_comuni_dict[str(id_comune) + delimiter + str(66)] = fc

                fc_81 = forecast_comuni_dict[str(id_comune) + delimiter + str(81)]
                wind_class_83 = wind_class_dict[
                    my_max(
                        forecast_comuni_dict[
                            str(id_comune) + delimiter + str(81)
                        ].wind_class.code,  # type: ignore
                        forecast_comuni_dict[
                            str(id_comune) + delimiter + str(82)
                        ].wind_class.code,  # type: ignore
                    )
                ]
                fc = models_w35.ForecastComuni(
                    id_comune=fc_81.id_comune,
                    id_time_layouts=time_layouts_dict[83],
                    wind_class=wind_class_83,
                )
                forecast_comuni_dict[str(id_comune) + delimiter + str(83)] = fc

            # debug
            # for fc in forecast_comuni_dict:
            #     print("fc", str(forecast_comuni_dict[fc].id_comune), str(forecast_comuni_dict[fc].id_time_layouts))

            # popolo il dizionario con i w15_data
            for w15 in w15_data_new_dict:
                # id_venue, id_parametro, id_aggregazione, id_time_layouts
                w15_keys = w15.split(delimiter)
                if (
                    str(id_venue_to_id_comune[int(w15_keys[0])])
                    + delimiter
                    + w15_keys[3]
                    in forecast_comuni_dict
                ):
                    fc = forecast_comuni_dict[
                        str(id_venue_to_id_comune[int(w15_keys[0])])
                        + delimiter
                        + w15_keys[3]
                    ]
                    if w15_keys[1] == "SKY_CONDIT":
                        if fc.sky_condition is not None:
                            w15_data_new_dict[w15].numeric_value = (
                                fc.sky_condition.id_sky_condition
                            )
                    elif w15_keys[1] == "TERMA":
                        if fc.air_temperature is not None:
                            w15_data_new_dict[w15].numeric_value = int(
                                fc.air_temperature
                            )
                        if fc.trend is not None:
                            w15_data_new_dict[w15].id_trend = (
                                fc.trend
                            )  # non ci sono trend su forecast_comuni
                    elif w15_keys[1] == "WIND_CLASS":
                        if fc.wind_class is not None:
                            w15_data_new_dict[w15].numeric_value = fc.wind_class.code
                    else:
                        print("w15 new: errore parametro non trovato", w15_keys[1])

        w15_data_list = []
        for w15d in w15_data_new_dict:
            w15_data_list.append(w15_data_new_dict[w15d])
        models.W15Data.objects.bulk_create(w15_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w15": new.id_w15})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W15.objects.get(pk=pk)
        print("w15 reopen:", old)
        old.status = "2"
        old_id_w15 = old.id_w15
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w15_parent = old_id_w15
        new.seq_num = old.seq_num + 1  # type: ignore
        new.save()
        # print('created: ', new)
        old_data = models.W15Data.objects.filter(id_w15=old_id_w15)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w15 = new
            new_data.save()

        return Response({"id_w15": new.id_w15})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w15/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w15 = snapshots["id_w15"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w15 = models.W15.objects.get(pk=id_w15)
        for snapshot in snapshots:
            setattr(w15, snapshot, snapshots[snapshot])
        w15.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W15SerializerFull(w15, context={"request": request})
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


class W15DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W15 bulletin Data to be viewed or edited
    """

    queryset = models.W15Data.objects.all()
    serializer_class = W15DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W15Data.objects
        w15Data = get_object_or_404(queryset, pk=pk)
        serializer = W15DataSerializer(w15Data, context={"request": request})
        return Response(serializer.data)


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%dT%H:%M:%S",
    )


class ParchiHTMLView(TemplateView):
    template_name = "parchi.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W15.objects
        w15 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W15SerializerFull(w15)
        w15 = serializer.data
        w15 = rearrange(w15)
        context = {"w15": w15}
        return context


class ParchiPDFView(ParchiHTMLView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="parchi.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class ParchiPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        django_url = os.getenv("DJANGO_URL", "http://django:8000")
        r = requests.get(django_url + "/w15/pdf/%d" % kwargs["pk"])

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


# 0 | Stazionario
# 1 | In Aumento
# 2 | In Diminuzione
map_trend = {None: "", 0: "=", 1: "+", 2: "-"}


def rearrange(w15):
    sky_condition_dict = {}
    sky_conditions = models_w05.SkyCondition.objects.all()
    for sky_condition in sky_conditions:
        sky_condition_dict[sky_condition.id_sky_condition] = sky_condition
    wind_class_dict = {}
    wind_classes = models_w35.WindClass.objects.all()
    for wind_class in wind_classes:
        wind_class_dict[wind_class.code] = wind_class
    locale.setlocale(locale.LC_TIME, "it_IT.UTF8")
    day0 = datetime.datetime.strptime(w15["data_emissione"], "%Y-%m-%dT%H:%M:%S")
    day1 = day0 + datetime.timedelta(days=1)
    day2 = day0 + datetime.timedelta(days=2)
    w15["day0"] = day0.strftime("%d %B %Y")
    w15["day1"] = day1.strftime("%d %B %Y")
    w15["day2"] = day2.strftime("%d %B %Y")
    w15["w15_data"] = {}
    for data in w15["w15data_set"]:
        if data["id_venue"] not in w15["w15_data"]:
            w15["w15_data"][data["id_venue"]] = {}
        if data["id_time_layouts"] not in w15["w15_data"][data["id_venue"]]:
            w15["w15_data"][data["id_venue"]][data["id_time_layouts"]] = {}
        if data["id_parametro"] not in w15["w15_data"][data["id_venue"]]:
            w15["w15_data"][data["id_venue"]][data["id_time_layouts"]][
                data["id_parametro"]
            ] = {}
        w15["w15_data"][data["id_venue"]][data["id_time_layouts"]][
            data["id_parametro"]
        ]["numeric_value"] = data["numeric_value"]
        if data["id_parametro"] == "SKY_CONDIT":
            w15["w15_data"][data["id_venue"]][data["id_time_layouts"]][
                data["id_parametro"]
            ]["sky_condition"] = sky_condition_dict[
                data["numeric_value"]
            ].description_ita
        if data["id_parametro"] == "WIND_CLASS":
            w15["w15_data"][data["id_venue"]][data["id_time_layouts"]][
                data["id_parametro"]
            ]["wind_class"] = wind_class_dict[data["numeric_value"]].descrizione
        if data["id_parametro"] == "TERMA":
            w15["w15_data"][data["id_venue"]][data["id_time_layouts"]][
                data["id_parametro"]
            ]["trend"] = map_trend[data["id_trend"]]
    return w15


class MandriaXmlView(TemplateView):
    template_name = "mandria.xml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W15.objects
        w15 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W15SerializerFull(w15)
        w15 = serializer.data
        w15 = rearrange(w15)
        context = {"w15": w15}
        return context


class StupinigiXmlView(TemplateView):
    template_name = "stupinigi.xml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W15.objects
        w15 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W15SerializerFull(w15)
        w15 = serializer.data
        w15 = rearrange(w15)
        context = {"w15": w15}
        return context
