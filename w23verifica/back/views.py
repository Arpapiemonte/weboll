#
# Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
#
#
# import csv
import datetime
import json
import os

# import tempfile
# from contextlib import closing
from os import getenv

import requests

# from django.contrib.auth.models import User
from django.db.transaction import atomic

# from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

# from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

# from rest_framework_xml.renderers import XMLRenderer
from wkhtmltopdf.views import PDFTemplateResponse

from w23.back import models as models_w23
from w23verifica.back import models
from w23verifica.back.serializers import (
    W23GiudizioSerializer,
    W23SeveritaSerializer,
    W23verificaCriticitaSerializer,
    W23VerificaDataSerializer,
    W23VerificaSerializer,
    W23VerificaSerializerFull,
    W23ZoneSerializer,
)
from website.common.tasks import send_with_celery
from website.common.views import (  # BulletinDraftLocked, ExistingTodayBulletin,
    StandardResultsSetPagination,
)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


# find maximum value among all parameters
def massimo(parameters):
    p = parameters.copy()
    p.pop("EFFETTI SUL TERRITORIO", "")
    lookup = {"BIANCO": -1, "VERDE": 0, "GIALLO": 1, "ARANCIONE": 2, "ROSSO": 3}
    m = max(p, key=lambda x: lookup[p[x]])
    return p[m]


class W23VerificaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletins to be viewed or edited
    """

    queryset = models.W23Verifica.objects.order_by("-last_update", "-pk")
    serializer_class = W23VerificaSerializer
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

    def retrieve(self, request, pk=None):
        queryset = models.W23Verifica.objects
        w23verifica = get_object_or_404(queryset, pk=pk)
        serializer = W23VerificaSerializerFull(
            w23verifica, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w23verifica = models.W23Verifica.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w23verifica.id_w23verifica,
            "del",
            w23verifica.data_emissione,
            "iniziato",
        )
        w23verifica.status = "1"
        w23verifica.username = request.user.username
        w23verifica.last_update = inizio
        w23verifica.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("verificaallerta", w23verifica.id_w23verifica)
        return Response({"id_w23verifica": w23verifica.id_w23verifica})

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        url_path="new/(?P<num_bollettino>[0-9]+(_[0-9]+)+)",
    )
    @atomic
    def new(self, request, num_bollettino):
        # print("new,num_bollettino-----------", num_bollettino)
        # delimiter_firstguess = ";"
        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)

        create_empty = False
        if (
            not models.W23Verifica.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w23verifica = (
                models.W23Verifica.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w23verifica = (
                models.W23Verifica.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w23verifica.id_w23verifica,
            "del",
            old_w23verifica.data_emissione,
            "iniziato",
        )
        # gestione anno nuovo
        if old_w23verifica.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            # numero_bollettino = 1

        if create_empty:
            situazione_evoluzione = "-Note:"
            note = "Nulla da segnalare oggi"
        else:
            situazione_evoluzione = str(old_w23verifica.situazione_evoluzione)
            note = "-"
        data_analisi = ""
        data_emissione = str(today)[:10]
        giudizio = 1
        id_numero_bollettino = "0_0"
        numero_bollettino = "0/0"
        url = (
            getenv("BASE_DATA_URL_FULL", "http://frontend:80")
            + "/allerta_valutazione_bollettino/allerta_valutazione_bollettino_"
            + num_bollettino
            + ".json"
        )
        num_bollettinotemp = num_bollettino.split("_")
        numero_bollettino = num_bollettinotemp[0] + "/" + num_bollettinotemp[1]
        # print("**************url", url)
        # controllo che il file ci sia
        try:

            response = requests.get(url)
            data = json.loads(response.text)
            id_numero_bollettino = data["num_bollettino"]
            data_analisi = str(data["data_bollettino"])[:10]
            fenomeni_oss_oggi = {}
            for area in data["d0"]:
                fenomeni_oss_oggi[area["cod_area"]] = {
                    "temporali_oggi": area["osservato"]["temporali"],
                    "idraulico_oggi": area["osservato"]["idraulico"],
                    "idrogeologico_oggi": area["osservato"]["idrogeologico"],
                    "neve_oggi": area["osservato"]["neve"],
                    "valanghe_oggi": area["osservato"]["valanghe"],
                }
            fenomeni_oss_domani = {}
            for area in data["d1"]:
                fenomeni_oss_domani[area["cod_area"]] = {
                    "temporali_domani": area["osservato"]["temporali"],
                    "idraulico_domani": area["osservato"]["idraulico"],
                    "idrogeologico_domani": area["osservato"]["idrogeologico"],
                    "neve_domani": area["osservato"]["neve"],
                    "valanghe_domani": area["osservato"]["valanghe"],
                }
            # print("-----------------fenomeni_oss_oggi-----------", fenomeni_oss_oggi)
        except Exception:
            pass
            print("url non esiste non la trovo", url)
        print("url esiste", url)
        new_w23 = None
        new_w23 = (
            models_w23.W23.objects.filter(status="1")
            .filter(numero_bollettino=str(numero_bollettino))
            .latest("pk")
        )

        # inizio lettura dati dell bollettino e inserimento in memoria
        new_w23_data = models_w23.W23Data.objects.filter(id_w23=new_w23.id_w23)
        new_w23_data_dict = {}

        for nwp in new_w23_data:
            new_w23_data_dict[str(nwp.id_w23_zone.id_w23_zone)] = {
                "idrogeologico_oggi": nwp.idrogeologico_oggi.id_w23_pericolo,
                "idrogeologico_domani": nwp.idrogeologico_domani.id_w23_pericolo,
                "idraulico_oggi": nwp.idraulico_oggi.id_w23_pericolo,
                "neve_oggi": nwp.neve_oggi.id_w23_pericolo,
                "valanghe_oggi": nwp.valanghe_oggi.id_w23_pericolo,
                "idraulico_domani": nwp.idraulico_domani.id_w23_pericolo,
                "temporali_oggi": nwp.temporali_oggi.id_w23_pericolo,
                "temporali_domani": nwp.temporali_domani.id_w23_pericolo,
                "neve_domani": nwp.neve_domani.id_w23_pericolo,
                "valanghe_domani": nwp.valanghe_domani.id_w23_pericolo,
            }

        criticita_dict = {
            "-": -2,
            "BIANCO": -1,
            "VERDE": 0,
            "GIALLO": 1,
            "ARANCIONE": 2,
            "ROSSO": 3,
        }
        criticita_dict_inv = {
            -2: "-",
            -1: "BIANCO",
            0: "VERDE",
            1: "GIALLO",
            2: "ARANCIONE",
            3: "ROSSO",
        }

        zone = models.W23Zone.objects.all()
        zone_dict = {}
        prev_max_crit_tot = {}
        prev_max_crit_tot_oggi = {}
        prev_max_crit_tot_domani = {}
        oss_max_crit_tot_oggi = {}
        oss_max_crit_tot_domani = {}
        oss_max_crit_tot = {}
        err_crit_tot = {}
        num_lievi = 0
        num_gravi_molto_gravi = 0
        for v in zone:
            zone_dict[str(v.id_w23_zone)] = v
            if str(v.id_w23_zone) != "12":
                prev_max_crit_tot_oggi[str(v.id_w23_zone)] = max(
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["temporali_oggi"]
                    ],
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["idraulico_oggi"]
                    ],
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["idrogeologico_oggi"]
                    ],
                    criticita_dict[new_w23_data_dict[str(v.id_w23_zone)]["neve_oggi"]],
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["valanghe_oggi"]
                    ],
                )
                prev_max_crit_tot_domani[str(v.id_w23_zone)] = max(
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["temporali_domani"]
                    ],
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["idraulico_domani"]
                    ],
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["idrogeologico_domani"]
                    ],
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["neve_domani"]
                    ],
                    criticita_dict[
                        new_w23_data_dict[str(v.id_w23_zone)]["valanghe_domani"]
                    ],
                )
                prev_max_crit_tot[str(v.id_w23_zone)] = max(
                    prev_max_crit_tot_oggi[str(v.id_w23_zone)],
                    prev_max_crit_tot_domani[str(v.id_w23_zone)],
                )
                oss_max_crit_tot_oggi[str(v.id_w23_zone)] = max(
                    criticita_dict[
                        fenomeni_oss_oggi[str(v.nome_zona)]["temporali_oggi"]
                    ],
                    criticita_dict[
                        fenomeni_oss_oggi[str(v.nome_zona)]["idraulico_oggi"]
                    ],
                    criticita_dict[
                        fenomeni_oss_oggi[str(v.nome_zona)]["idrogeologico_oggi"]
                    ],
                    criticita_dict[fenomeni_oss_oggi[str(v.nome_zona)]["neve_oggi"]],
                    criticita_dict[
                        fenomeni_oss_oggi[str(v.nome_zona)]["valanghe_oggi"]
                    ],
                )
                oss_max_crit_tot_domani[str(v.id_w23_zone)] = max(
                    criticita_dict[
                        fenomeni_oss_domani[str(v.nome_zona)]["temporali_domani"]
                    ],
                    criticita_dict[
                        fenomeni_oss_domani[str(v.nome_zona)]["idraulico_domani"]
                    ],
                    criticita_dict[
                        fenomeni_oss_domani[str(v.nome_zona)]["idrogeologico_domani"]
                    ],
                    criticita_dict[
                        fenomeni_oss_domani[str(v.nome_zona)]["neve_domani"]
                    ],
                    criticita_dict[
                        fenomeni_oss_domani[str(v.nome_zona)]["valanghe_domani"]
                    ],
                )
                oss_max_crit_tot[str(v.id_w23_zone)] = max(
                    oss_max_crit_tot_oggi[str(v.id_w23_zone)],
                    oss_max_crit_tot_domani[str(v.id_w23_zone)],
                )
                # Calcolo severità
                if oss_max_crit_tot[str(v.id_w23_zone)] == prev_max_crit_tot[
                    str(v.id_w23_zone)
                ] or (criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]] == "-"):
                    err_crit_tot[str(v.id_w23_zone)] = 1
                elif (
                    (
                        criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]]
                        == "VERDE"
                        and criticita_dict_inv[prev_max_crit_tot[str(v.id_w23_zone)]]
                        == "GIALLO"
                    )
                    or (
                        criticita_dict_inv[prev_max_crit_tot[str(v.id_w23_zone)]]
                        == "VERDE"
                        and criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]]
                        == "GIALLO"
                    )
                    or (
                        criticita_dict_inv[prev_max_crit_tot[str(v.id_w23_zone)]]
                        == "ARANCIONE"
                        and criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]]
                        == "GIALLO"
                    )
                ):
                    err_crit_tot[str(v.id_w23_zone)] = 2
                    num_lievi = num_lievi + 1
                elif (
                    (
                        criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]]
                        == "ARANCIONE"
                        and criticita_dict_inv[prev_max_crit_tot[str(v.id_w23_zone)]]
                        == "GIALLO"
                    )
                    or (
                        criticita_dict_inv[prev_max_crit_tot[str(v.id_w23_zone)]]
                        == "ARANCIONE"
                        and criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]]
                        == "VERDE"
                    )
                    or (
                        criticita_dict_inv[prev_max_crit_tot[str(v.id_w23_zone)]]
                        == "ROSSO"
                        and criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]]
                        == "ARANCIONE"
                    )
                    or (
                        criticita_dict_inv[oss_max_crit_tot[str(v.id_w23_zone)]]
                        == "ROSSO"
                        and criticita_dict_inv[prev_max_crit_tot[str(v.id_w23_zone)]]
                        == "ARANCIONE"
                    )
                ):
                    err_crit_tot[str(v.id_w23_zone)] = 3
                    num_gravi_molto_gravi = num_gravi_molto_gravi + 1
                else:
                    err_crit_tot[str(v.id_w23_zone)] = 4
                    num_gravi_molto_gravi = num_gravi_molto_gravi + 1
                # Fine Calcolo severità
                # print(
                #     "++++++++++++++++++++err_crit_tot[str(v.id_w23_zone)]",
                #     v.id_w23_zone,
                #     err_crit_tot[str(v.id_w23_zone)],
                # )
        # print("++++++++++++++++++++num_lievi", num_lievi)
        # print("+++++++++++++++++++++++++++num_gravi_molto_gravi", num_gravi_molto_gravi)
        # Calcolo giudizio
        giudizio = 5
        if (num_gravi_molto_gravi == 1 and num_lievi == 0) or (
            num_gravi_molto_gravi <= 1 and num_lievi >= 1 and num_lievi <= 3
        ):
            giudizio = 2
        if num_gravi_molto_gravi == 0 and num_lievi == 0:
            giudizio = 1
        if (
            num_gravi_molto_gravi >= 2 and num_gravi_molto_gravi <= 3 and num_lievi == 0
        ) or (num_gravi_molto_gravi <= 2 and num_lievi >= 4 and num_lievi <= 6):
            giudizio = 3
        if (
            (
                num_gravi_molto_gravi >= 4
                and num_gravi_molto_gravi <= 6
                and num_lievi <= 3
            )
            or (
                num_gravi_molto_gravi >= 2
                and num_gravi_molto_gravi <= 3
                and num_lievi <= 6
                and num_lievi >= 1
            )
            or (num_gravi_molto_gravi <= 2 and num_lievi >= 7)
        ):
            giudizio = 4

        # print("++++++++++++++++++++giudizio", giudizio)
        # Fine Calcolo giudizio
        new = models.W23Verifica(
            data_emissione=data_analisi,
            data_analisi=data_emissione,
            situazione_evoluzione=situazione_evoluzione,
            annotazione=note,
            status=0,
            last_update=datetime.datetime.now(),
            username=request.user,
            id_numero_bollettino=id_numero_bollettino,
            numero_bollettino=numero_bollettino,
            id_w23giudizio=giudizio,  # da prendere esternamente
        )
        new.save()
        try:
            # carico la configurazione json per sapere quanti record ci devono essere su w23verifica_data
            with open("config/w23verifica_data.json") as json_file:
                w23verifica_data_config = json.load(json_file)
            # riempo il dizionario con i dati del json di default
            w23verifica_data_new_dict = {}
            for w in w23verifica_data_config:
                w23verifica_data_new_dict[w23verifica_data_config[w]["id_w23_zone"]] = (
                    models.W23VerificaData(
                        id_w23verifica=new,
                        id_w23_zone=zone_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ],
                        prev_crit_idraulico_oggi=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["idraulico_oggi"],
                        oss_crit_idraulico_oggi=fenomeni_oss_oggi[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["idraulico_oggi"],
                        prev_crit_idraulico_domani=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["idraulico_domani"],
                        oss_crit_idraulico_domani=fenomeni_oss_domani[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["idraulico_domani"],
                        prev_crit_idrogeologico_oggi=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["idrogeologico_oggi"],
                        oss_crit_idrogeologico_oggi=fenomeni_oss_oggi[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["idrogeologico_oggi"],
                        prev_crit_idrogeologico_domani=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["idrogeologico_domani"],
                        oss_crit_idrogeologico_domani=fenomeni_oss_domani[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["idrogeologico_domani"],
                        prev_crit_temporali_oggi=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["temporali_oggi"],
                        oss_crit_temporali_oggi=fenomeni_oss_oggi[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["temporali_oggi"],
                        prev_crit_temporali_domani=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["temporali_domani"],
                        oss_crit_temporali_domani=fenomeni_oss_domani[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["temporali_domani"],
                        prev_crit_neve_oggi=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["neve_oggi"],
                        oss_crit_neve_oggi=fenomeni_oss_oggi[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["neve_oggi"],
                        prev_crit_neve_domani=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["neve_domani"],
                        oss_crit_neve_domani=fenomeni_oss_domani[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["neve_domani"],
                        prev_crit_valanghe_oggi=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["valanghe_oggi"],
                        oss_crit_valanghe_oggi=fenomeni_oss_oggi[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["valanghe_oggi"],
                        prev_crit_valanghe_domani=new_w23_data_dict[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ]["valanghe_domani"],
                        oss_crit_valanghe_domani=fenomeni_oss_domani[
                            str(w23verifica_data_config[w]["w23_zone"])
                        ]["valanghe_domani"],
                        prev_crit_tot=criticita_dict_inv[
                            prev_max_crit_tot[
                                str(w23verifica_data_config[w]["id_w23_zone"])
                            ]
                        ],
                        oss_crit_tot=criticita_dict_inv[
                            oss_max_crit_tot[
                                str(w23verifica_data_config[w]["id_w23_zone"])
                            ]
                        ],
                        err_crit_tot=err_crit_tot[
                            str(w23verifica_data_config[w]["id_w23_zone"])
                        ],
                        prev_crit_oggi=criticita_dict_inv[
                            prev_max_crit_tot_oggi[
                                str(w23verifica_data_config[w]["id_w23_zone"])
                            ]
                        ],
                        oss_crit_oggi=criticita_dict_inv[
                            oss_max_crit_tot_oggi[
                                str(w23verifica_data_config[w]["id_w23_zone"])
                            ]
                        ],
                        err_crit_oggi=w23verifica_data_config[w]["err_crit_oggi"],
                        prev_crit_domani=criticita_dict_inv[
                            prev_max_crit_tot_domani[
                                str(w23verifica_data_config[w]["id_w23_zone"])
                            ]
                        ],
                        oss_crit_domani=criticita_dict_inv[
                            oss_max_crit_tot_domani[
                                str(w23verifica_data_config[w]["id_w23_zone"])
                            ]
                        ],
                        err_crit_domani=w23verifica_data_config[w]["err_crit_domani"],
                    )
                )
        except Exception:
            pass
            print("url non esiste non la trovo data")
        # print("new_w23.id_w23", new_w23.id_w23)
        print("url esiste data")
        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w23verifica_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w23verifica_data_list = []
        for w in w23verifica_data_new_dict:
            w23verifica_data_list.append(w23verifica_data_new_dict[w])
        models.W23VerificaData.objects.bulk_create(w23verifica_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w23verifica": new.id_w23verifica})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w23verifica/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w23verifica = snapshots["id_w23verifica"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w23verifica = models.W23Verifica.objects.get(pk=id_w23verifica)
        for snapshot in snapshots:
            setattr(w23verifica, snapshot, snapshots[snapshot])
        w23verifica.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W23VerificaSerializerFull(
            w23verifica, context={"request": request}
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


class W23GiudizioView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Tendenza to be viewed
    """

    queryset = models.W23Giudizio.objects.order_by("id_w23giudizio")
    serializer_class = W23GiudizioSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W23SeveritaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Criticità to be viewed
    """

    queryset = models.W23Severita.objects.order_by("id_w23severita")
    serializer_class = W23SeveritaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W23VerificaDataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Data to be viewed or edited
    """

    queryset = models.W23VerificaData.objects.all()
    serializer_class = W23VerificaDataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W23VerificaData.objects
        w23verificaData = get_object_or_404(queryset, pk=pk)
        serializer = W23VerificaDataSerializer(
            w23verificaData, context={"request": request}
        )

        return Response(serializer.data)


class W23ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Zone to be viewed or edited
    """

    queryset = models.W23Zone.objects.all()
    serializer_class = W23ZoneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W23verificaCriticitaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W23 bulletin Criticità to be viewed
    """

    queryset = models.W23verificaCriticita.objects.all()
    serializer_class = W23verificaCriticitaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class VerificaAllertaHTMLView(TemplateView):
    template_name = "verificaallerta.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W23Verifica.objects
        w23verifica = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W23VerificaSerializerFull(w23verifica)
        verificaallerta = serializer.data

        context = {
            "verificaallerta": verificaallerta,
            "title": "Bollettino verifica allerta",
        }
        return context


class VerificaAllertaPDFView(VerificaAllertaHTMLView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="verificaallerta.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response
