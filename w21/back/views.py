#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
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

# from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w21.back import models
from w21.back.serializers import W21DataSerializer, W21Serializer, W21SerializerFull
from website.common.tasks import send_with_celery
from website.common.views import (  # ExistingTodayBulletin,
    BulletinDraftLocked,
    StandardResultsSetPagination,
)
from website.core import models as models_w05


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W21View(viewsets.ModelViewSet):
    """
    API endpoint that allows W21 bulletins to be viewed or edited
    """

    queryset = models.W21.objects.order_by("-last_update", "-pk")
    serializer_class = W21Serializer
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
        queryset = models.W21.objects
        w21 = get_object_or_404(queryset, pk=pk)
        serializer = W21SerializerFull(w21, context={"request": request})
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.username != self.request.user.username:
            raise BulletinDraftLocked()
        queryset = models.W21.objects
        if (
            instance.id_w21_parent
            and queryset.filter(pk=instance.id_w21_parent).exists()
        ):
            w21 = get_object_or_404(queryset, pk=instance.id_w21_parent)
            w21.status = "1"
            if not User.objects.filter(username=w21.username).exists():
                print("perform_destroy non trovo l'utente " + w21.username)
                w21.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w21.save()
        instance.delete()

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w21 = models.W21.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w21.id_w21,
            "del",
            w21.data_emissione,
            "iniziato",
        )
        w21.status = "1"
        w21.username = request.user.username
        w21.last_update = inizio
        w21.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("strade_di_biella", w21.id_w21)
        return Response({"id_w21": w21.id_w21})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        # creazione del bollettino odierno
        now = datetime.datetime.now()
        today = datetime.datetime.today()
        # tomorrow = today + datetime.timedelta(days=1)
        maptl = {
            50: 46,  # massima D0
            68: 60,  # minima D1
            67: 62,  # massima D1
            85: 81,  # minima D2
            84: 82,  # massima D2
        }
        delimiter = "__"

        def HashW21Data(id_venue, id_parametro, id_aggregazione, id_time_layouts):
            return (
                str(id_venue)
                + delimiter
                + id_parametro
                + delimiter
                + str(id_aggregazione)
                + delimiter
                + str(id_time_layouts)
            )

        new = models.W21(
            data_emissione=today,
            status="0",  # il nuovo bollettino lo metto in bozza
            last_update=now,
            username=request.user,
        )
        new.save()

        # leggo venues
        venues = models.Venue.objects.all()
        venues_dict = {}
        for v in venues:
            venues_dict[str(v.id_venue)] = v

        # leggo time layouts
        time_layouts = models.TimeLayouts.objects.all()
        time_layouts_dict = {}
        for t in time_layouts:
            time_layouts_dict[str(t.id_time_layouts)] = t

        # leggo parametro
        parametri = models.Parametro.objects.all().select_related("id_unita_misura")
        parametri_dict = {}
        for p in parametri:
            parametri_dict[p.id_parametro] = p

        # leggo aggregazione
        aggregazione = models.Aggregazione.objects.all().select_related(
            "id_unita_misura"
        )
        aggregazione_dict = {}
        for a in aggregazione:
            aggregazione_dict[str(a.id_aggregazione)] = a

        # leggo weather_values
        fine = datetime.datetime.now()
        print(
            "leggo weather_values ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        weather_values = models_w05.WeatherValues.objects.all().select_related(
            "id_venue", "id_parametro", "id_aggregazione", "id_time_layouts"
        )
        weather_values_dict = {}
        for w in weather_values:
            weather_values_dict[
                HashW21Data(
                    w.id_venue.id_venue,
                    w.id_parametro.id_parametro,
                    w.id_aggregazione.id_aggregazione,
                    w.id_time_layouts.id_time_layouts,
                )
            ] = w

        # carico la configurazione json per sapere quanti record ci devono essere su w21_data
        with open("config/w21_data.json") as json_file:
            w21_data_config = json.load(json_file)

        # sistema il json di configurazione in modo da avere come chiave primaria
        # id_venue__id_parametro__id_aggregazione__id_time_layouts
        w21_data_da_inserire = {}  # type: ignore
        for w in w21_data_config:
            w21_data_da_inserire[
                HashW21Data(
                    w21_data_config[w]["id_venue"],
                    w21_data_config[w]["id_parametro"],
                    w21_data_config[w]["id_aggregazione"],
                    w21_data_config[w]["id_time_layouts"],
                )
            ] = None
        # creo tutti i w21_data nuovi
        w21_data_new_dict: dict = {}
        for w in w21_data_da_inserire:
            w21_data_tmp = w.split(delimiter)  # type: ignore
            my_time_layouts = time_layouts_dict[w21_data_tmp[3]]
            w21_data_new_dict[
                HashW21Data(
                    w21_data_tmp[0], w21_data_tmp[1], w21_data_tmp[2], w21_data_tmp[3]
                )
            ] = models.W21Data(
                id_w21=new,
                id_venue=venues_dict[w21_data_tmp[0]],
                id_parametro=parametri_dict[w21_data_tmp[1]],
                id_aggregazione=aggregazione_dict[w21_data_tmp[2]],
                numeric_value=None,
                id_trend=None,
                id_time_layouts=my_time_layouts,
            )

        # with open("config/skycond_firstguess.json") as json_file:
        #    firstguessdict = json.load(json_file)
        #   skycond_to_pluv = firstguessdict["skycond_to_pluv"]

        # leggo i valori da weather_values per w21_data
        fine = datetime.datetime.now()
        print(
            "inizio carica weather_values per w21_data",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        for w in weather_values_dict:
            w_keys = w.split(delimiter)  # type: ignore
            # leggo tutti i parametri ad eccezione della temperatura perchè
            # usa tl differenti
            if (
                HashW21Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                in w21_data_new_dict
            ):
                w21_data_new_dict[
                    HashW21Data(w_keys[0], w_keys[1], w_keys[2], w_keys[3])
                ].numeric_value = weather_values_dict[w].original_numeric_values

            # ora controllo i tl della temperatura
            if w_keys[1] == "TERMA":
                if int(w_keys[3]) in maptl.keys():
                    new_keytl = maptl[int(w_keys[3])]
                    # print(w_keys[3], new_keytl)
                    if (
                        HashW21Data(w_keys[0], w_keys[1], w_keys[2], new_keytl)
                        in w21_data_new_dict
                    ):
                        w21_data_new_dict[
                            HashW21Data(w_keys[0], w_keys[1], w_keys[2], new_keytl)
                        ].numeric_value = weather_values_dict[w].original_numeric_values

                    # if weather_values_dict[w].original_trend is not None:
                    #    w21_data_new_dict[
                    #        HashW21Data(w_keys[0], w_keys[1], w_keys[2], new_keytl)
                    #    ].id_trend = weather_values_dict[
                    #        w
                    #    ].original_trend.id_trend  # type: ignore
        # salvataggio w21_data
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w21_data ",
            abs((fine - now).total_seconds()),
            "secondi",
        )
        w21_data_list = []
        for w in w21_data_new_dict:
            w21_data_list.append(w21_data_new_dict[w])

        models.W21Data.objects.bulk_create(w21_data_list)

        print("created: ", new)
        return Response({"id_w21": new.id_w21})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W21.objects.get(pk=pk)
        print("w21 reopen:", old)
        old.status = "2"
        old_id_w21 = old.id_w21
        old.save()
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.last_update = now
        new.username = request.user
        new.id_w21_parent = old_id_w21
        new.save()
        # print('created: ', new)
        old_data = models.W21Data.objects.filter(id_w21=old_id_w21)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w21 = new
            new_data.save()

        return Response({"id_w21": new.id_w21})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== SONO NEL BULK_UPDATE del backend")
        print("========== POST /w21/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        # print("snapshots", snapshots)
        id_w21 = next(s["id"] for s in snapshots if s["id_key"] == "id_w21")
        last_update = datetime.datetime.now()
        last_update_snapshot = {
            "id_key": "id_w21",
            "id": id_w21,
            "value_key": "last_update",
            "new_value": last_update,
        }
        snapshots.append(last_update_snapshot)
        w21 = models.W21.objects.get(pk=id_w21)
        for snapshot in snapshots:
            if snapshot["id_key"] == "id_w21":
                # print(
                #     "id_w21:",
                #     snapshot["id"],
                #     snapshot["value_key"],
                #     snapshot["new_value"],
                # )
                setattr(w21, snapshot["value_key"], snapshot["new_value"])
                updated += 1
            else:
                # print(
                #     "id_w21_data:",
                #     snapshot["id"],
                #     "value_key:",
                #     snapshot["value_key"],
                #     "numeric_value",
                #     snapshot["new_value"],
                # )
                data = models.W21Data.objects.get(pk=snapshot["id"])
                data.numeric_value = snapshot["new_value"]
                data.save()
                updated += 1
        w21.save()
        fine = datetime.datetime.now()
        serializer = W21SerializerFull(w21, context={"request": request})
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


class W21DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows w21 bulletin Data to be viewed or edited
    """

    queryset = models.W21Data.objects.all()
    serializer_class = W21DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W21Data.objects
        w21Data = get_object_or_404(queryset, pk=pk)
        serializer = W21DataSerializer(w21Data, context={"request": request})
        return Response(serializer.data)


def convert_to_date(d, k):
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


class W21SVGView(TemplateView):
    template_name = "biella.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W21.objects
        w21 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W21SerializerFull(w21)
        autostrada = serializer.data
        convert_to_date(autostrada, "data_emissione")
        days = []

        dayDate = autostrada["data_emissione"]
        for r in range(3):
            day = dayDate.strftime("%d/%m/%Y")
            days.append(day)
            dayDate = dayDate + datetime.timedelta(days=1)

        venue = models.Venue.objects.all()
        venue_dict = {}
        for m in venue:
            if m.id_venue in (179, 180, 181, 182, 183):
                venue_dict[str(m.id_venue)] = m.description

        sky_conditions = models_w05.SkyCondition.objects.all()
        sky_conditions_dict = {}
        for mmm in sky_conditions:
            sky_conditions_dict[mmm.id_sky_condition] = mmm

        # print("sky_conditions_dict", sky_conditions_dict)
        precipitation_classes = {
            "0": "Assente",
            "1": "Debole",
            "2": "Moderata",
            "3": "Forte",
            "4": "Molto forte",
        }

        biella_rearranged = {}  # type: ignore
        for data in autostrada["w21data_set"]:
            if data["id_venue"] not in biella_rearranged:
                biella_rearranged[data["id_venue"]] = {}
            if data["id_time_layouts"] not in biella_rearranged[data["id_venue"]]:
                biella_rearranged[data["id_venue"]][data["id_time_layouts"]] = {}
            if data["id_parametro"] not in biella_rearranged[data["id_venue"]]:
                biella_rearranged[data["id_venue"]][data["id_time_layouts"]][
                    data["id_parametro"]
                ] = {}
            if data["id_parametro"] == "PREC_CLASS":
                biella_rearranged[data["id_venue"]][data["id_time_layouts"]][
                    data["id_parametro"]
                ] = precipitation_classes[str(int(data["numeric_value"]))]
            elif data["id_parametro"] == "SKY_CONDIT":
                biella_rearranged[data["id_venue"]][data["id_time_layouts"]][
                    data["id_parametro"]
                ] = sky_conditions_dict[int(data["numeric_value"])]
            else:
                biella_rearranged[data["id_venue"]][data["id_time_layouts"]][
                    data["id_parametro"]
                ] = int(data["numeric_value"])
        # print("rearr", biella_rearranged)

        context = {
            "venues": venue_dict,
            "biella": autostrada,
            "bielladata": biella_rearranged,
            "days": days,
            "title": "Strade Provincia di Biella",
        }
        return context


class W21PDFView(W21SVGView):
    def get(self, request, *args, **kwargs):
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="w21.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class W21PngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        r = requests.get("http://django:8000/w21/pdf/%d" % kwargs["pk"])
        # print("--------------------------------------r", r)
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(r.content)
            f.flush()
            png_name = "%s.png" % f.name
            # print("png_name", png_name)
            command = "convert -verbose -density 145 -crop 1191x1685+3x5 %s %s" % (
                f.name,
                png_name,
            )
            # print("command", command)
            retcode = call(command, shell=True)
            # print("retcode", retcode)
            if retcode != 0:
                error = "imagemagick convert failed with code: %d" % retcode
                raise Exception(error)
            with open(png_name, mode="rb") as png_file:
                png_content = png_file.read()
            os.remove(png_name)
            return HttpResponse(
                content=memoryview(png_content), content_type="image/png"
            )
