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

from w22.back import models
from w22.back.serializers import (
    W22CriticitaSerializer,
    W22DataSerializer,
    W22Serializer,
    W22SerializerFull,
    W22TendenzaSerializer,
    W22ZoneSerializer,
)
from website.common.tasks import send_with_celery
from website.common.views import BulletinDraftLocked, StandardResultsSetPagination

# from contextlib import closing

# import os
# import tempfile
# from subprocess import call
# import requests


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W22View(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletins to be viewed or edited
    """

    queryset = models.W22.objects.order_by("-last_update", "-pk")
    serializer_class = W22Serializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        month = request.query_params.get("month", "all")
        year = request.query_params.get("year", "all")
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
        queryset = models.W22.objects
        if (
            instance.id_w22_parent
            and queryset.filter(pk=instance.id_w22_parent).exists()
        ):
            w22 = get_object_or_404(queryset, pk=instance.id_w22_parent)
            w22.status = "1"
            if not User.objects.filter(username=w22.username).exists():
                print("perform_destroy non trovo l'utente " + w22.username)
                w22.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w22.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W22.objects
        w22 = get_object_or_404(queryset, pk=pk)
        serializer = W22SerializerFull(w22, context={"request": request})
        return Response(serializer.data)

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W22.objects.get(pk=pk)
        print("w22 reopen:", old)
        old.status = "2"
        old_id_w22 = old.id_w22
        old.save()
        numero_bollettino = int(old.numero_bollettino.split("/")[0])
        # numero_bollettino = numero_bollettino + 1
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.numero_bollettino = (
            str(numero_bollettino) + "/" + str(datetime.datetime.today().year)
        )
        new.last_update = now
        new.username = request.user
        new.id_w22_parent = old_id_w22
        new.save()
        print("created: ", new)
        old_data = models.W22Data.objects.filter(id_w22=old_id_w22)
        for data in old_data:
            new_data = data
            new_data.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            new_data.id_w22 = new
            new_data.save()

        return Response({"id_w22": new.id_w22})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w22 = models.W22.objects.get(pk=pk)
        print(
            "send del bollettino ",
            w22.id_w22,
            "del",
            w22.data_emissione,
            "iniziato",
        )
        w22.status = "1"
        w22.username = request.user.username
        w22.last_update = inizio
        w22.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("piene", w22.id_w22)
        return Response({"id_w22": w22.id_w22})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send_auto(self, request, pk):
        w22 = models.W22.objects.get(pk=pk)
        print(
            "send_auto del bollettino ",
            w22.id_w22,
            "del",
            w22.data_emissione,
            "iniziato",
        )
        send_with_celery("piene", w22.id_w22, True)
        return Response({"id_w22": w22.id_w22})

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        inizio = datetime.datetime.now()
        today = datetime.datetime.today()
        emissione = today
        h_emissione = inizio.hour
        ora_emissione = str(h_emissione) + ":00"
        today = datetime.datetime.combine(
            today, datetime.datetime.min.time()
        )  # porto today alle 00:00
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = emissione + datetime.timedelta(days=1)
        create_empty = False

        # se non ho il bollettino di ieri allora ne creo uno vuoto????
        if (
            not models.W22.objects.filter(data_emissione=yesterday.date())
            .filter(status="1")
            .exists()
        ):
            create_empty = True
            print("new creazione bollettino vuoto!")

        if create_empty:
            old_w22 = (
                models.W22.objects.filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        else:
            old_w22 = (
                models.W22.objects.filter(data_emissione=yesterday.date())
                .filter(status="1")
                .order_by("-last_update")
                .latest("pk")
            )
        print(
            "new del bollettino ",
            old_w22.id_w22,
            "del",
            old_w22.data_emissione,
            "iniziato",
        )
        # aumento il sequenziale perchè è una nuova emissione
        numero_bollettino = int(old_w22.numero_bollettino.split("/")[0])
        numero_bollettino = numero_bollettino + 1
        # gestione anno nuovo
        if old_w22.data_emissione.year < today.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            numero_bollettino = 1

        if create_empty:
            annotazione = "-"
            situazione_evoluzione = "note:"
        else:
            annotazione = str(old_w22.annotazione)
            situazione_evoluzione = str(old_w22.situazione_evoluzione)

        new = models.W22(
            data_emissione=emissione.date(),
            data_validita=tomorrow,
            validita="36 ore",
            annotazione=annotazione,
            situazione_evoluzione=situazione_evoluzione,
            status=0,
            pdf_ordinario=1,
            ora_emissione=ora_emissione,
            last_update=datetime.datetime.now(),
            username=request.user,
            numero_bollettino=str(numero_bollettino) + "/" + str(today.year),
        )
        new.save()

        zone = models.W22Zone.objects.all()
        zone_dict = {}
        for v in zone:
            zone_dict[str(v.id_w22_zone)] = v
        # carico la configurazione json per sapere quanti record ci devono essere su w22_data
        with open("config/w22_data.json") as json_file:
            w22_data_config = json.load(json_file)
        # riempo il dizionario con i dati del json di default
        w22_data_new_dict = {}
        massimo_valore = None
        massimo_data = None
        liv_1 = None
        liv_2 = None
        liv_3 = None
        portata = None
        portata_6 = None
        tendenza6hprecedenti = None
        maxvalore12 = None
        maxvalore24 = None
        maxvalore36 = None
        # inizio lettura tabella MeteoRealTimeIdro e inserimento in memoria
        mrts = models.MeteoRealTimeIdro.objects.all()
        mrts_dict = {}
        for mrt in mrts:
            secondi = datetime.datetime.strptime(
                str(mrt.data) + " " + str(mrt.ora), "%Y-%m-%d %H:%M:%S"
            ).strftime("%s")
            mrts_dict[
                str(mrt.codice_istat_comune)
                + "#"
                + str(mrt.progr_punto_com)
                + "#"
                + str(mrt.id_parametro)
                + "#"
                + str(mrt.data)
                + "#"
                + str(mrt.ora)
                + "#"
                + str(secondi)
            ] = mrt.valore_validato
        # fine lettura tabella MeteoRealTimeIdro e inserimento in memoria

        # inizio lettura tabella Previsioni_idrologiche_nwp e inserimento in memoria
        nwps = models.Previsioni_idrologiche_nwp.objects.all()
        nwps_dict = {}
        for nwp in nwps:
            secondi = datetime.datetime.strptime(
                str(nwp.dataora), "%Y-%m-%d %H:%M:%S"
            ).strftime("%s")
            if nwp.id_parametro is not None:
                idp = nwp.id_parametro[0:4]
            else:
                idp = "XXXX"
            nwps_dict[
                str(nwp.codice)
                + "#"
                + idp
                + "#"
                + str(nwp.dataora)
                + "#"
                + str(secondi)
            ] = nwp.valore
        # fine lettura tabella Previsioni_idrologiche_nwp e inserimento in memoria

        # inizio lettura tabella MassimiStoriciIdrologici e inserimento in memoria
        mstis = models.MassimiStoriciIdrologici.objects.all()
        mstis_dict = {}
        for msti in mstis:
            secondi = datetime.datetime.strptime(str(msti.data), "%Y-%m-%d").strftime(
                "%s"
            )
            mstis_dict[
                str(msti.codice_istat_comune)
                + "#"
                + str(int(msti.progr_punto_com))
                + "#"
                + str(msti.id_parametro[0:4])
                + "#"
                + str(msti.data)
                + "#"
                + str(secondi)
            ] = msti.valore
        # fine lettura tabella MassimiStoriciIdrologici e inserimento in memoria

        # inizio lettura tabella SoglieIdrometriche e inserimento in memoria
        sogls = models.SoglieIdrometriche.objects.all()
        sogls_dict = {}  # type: ignore
        for sogl in sogls:
            sogls_dict[
                str(sogl.codice_istat_comune)
                + "#"
                + str(int(sogl.progr_punto_com))
                + "#"
                + str(sogl.id_parametro[0:4])
                + "#"
                + str(sogl.codice1)
                + "#"
                + str(sogl.codice2)
                + "#"
                + str(sogl.codice3)
            ] = None
        # fine lettura tabella SoglieIdrometriche e inserimento in memoria

        for w in w22_data_config:
            # variabili di ricerca
            codice_istat_comune = zone_dict[
                str(w22_data_config[w]["id_w22_zone"])
            ].codice_istat_comune
            progr_punto_com = str(
                zone_dict[str(w22_data_config[w]["id_w22_zone"])].progr_punto_com
            )
            id_parametro = zone_dict[
                str(w22_data_config[w]["id_w22_zone"])
            ].id_parametro
            codice = codice_istat_comune + progr_punto_com
            if id_parametro is not None:
                idp = id_parametro[0:4]
            else:
                idp = "XXXX"
            # inizio ricerca massimi in 12 24 e 36 da modello
            dati_staz = dict(
                filter(
                    lambda val: (
                        val[0].split("#")[0] == codice and val[0].split("#")[1] == idp
                    ),
                    nwps_dict.items(),
                )
            )
            # fine ricerca massimi in 12 24 e 36 da modello
            if len(dati_staz) > 0:
                # ordinamento in base a data e ora
                dati_staz_sorted = sorted(
                    dati_staz.items(), key=lambda v: int(v[0].split("#")[3])
                )

                # riempimento dati per ogni periodo temporale
                dati_max_12 = dict(dati_staz_sorted[:12])
                dati_max_24 = dict(dati_staz_sorted[11:24])
                dati_max_36 = dict(dati_staz_sorted[23:36])

                # ricerca del massimo
                maxvalore12 = max(dati_max_12.items(), key=lambda v: v[1])[1]
                maxvalore24 = max(dati_max_24.items(), key=lambda v: v[1])[1]
                maxvalore36 = max(dati_max_36.items(), key=lambda v: v[1])[1]

                if maxvalore12 is None:
                    maxvalore12 = 0
                if maxvalore24 is None:
                    maxvalore24 = 0
                if maxvalore36 is None:
                    maxvalore36 = 0
            else:
                maxvalore12 = 0
                maxvalore24 = 0
                maxvalore36 = 0

            # ricerco il valore e la data nei massimi storici
            dati_staz = dict(
                filter(
                    lambda val: (  # type: ignore
                        val[0].split("#")[0] == codice_istat_comune
                        and val[0].split("#")[1] == progr_punto_com
                        and val[0].split("#")[2] == idp
                    ),
                    mstis_dict.items(),
                )
            )
            # fine ricerco il valore e la data nei massimi storici
            massimo_valore = "n.d."
            massimo_data = None
            if len(dati_staz) > 0:
                # ordinamento dei dati in base alla data
                dati_staz_sorted = sorted(
                    dati_staz.items(),
                    key=lambda v: float(v[1]),
                    reverse=True,
                )
                # asseganzione dei valori
                massimo_valore = str(dati_staz_sorted[0][1])
                massimo_data = dati_staz_sorted[0][0].split("#")[3]
            # ricerca delle tre soglie idrometriche
            dati_staz = dict(
                filter(
                    lambda val: (  # type: ignore
                        val[0].split("#")[0] == codice_istat_comune
                        and val[0].split("#")[1] == progr_punto_com
                        and val[0].split("#")[2] == idp
                    ),
                    sogls_dict.items(),
                )
            )
            # fine ricerco delle tre soglie idrometriche
            if len(dati_staz) > 0:
                # asseganzione dei valori
                if list(dati_staz)[0].split("#")[3] == "None":
                    liv_1 = "n.d."
                else:
                    liv_1 = float(list(dati_staz)[0].split("#")[3])  # type: ignore
                if list(dati_staz)[0].split("#")[4] == "None":
                    liv_2 = "n.d."
                else:
                    liv_2 = float(list(dati_staz)[0].split("#")[4])  # type: ignore
                if list(dati_staz)[0].split("#")[5] == "None":
                    liv_3 = "n.d."
                else:
                    liv_3 = float(list(dati_staz)[0].split("#")[5])  # type: ignore
            else:
                liv_1 = "n.d."
                liv_2 = "n.d."
                liv_3 = "n.d."
            # ricerco i valori di portata attuale e di 6 ore prima in meteorealtime
            dati_staz = dict(
                filter(
                    lambda val: (  # type: ignore
                        val[0].split("#")[0] == codice_istat_comune
                        and val[0].split("#")[1] == progr_punto_com
                        and val[0].split("#")[2] == id_parametro
                    ),
                    mrts_dict.items(),
                )
            )
            # fine ricerco i valori di portata attuale e di 6 ore prima in meteorealtime
            portata = "n.d."
            portata_6 = "n.d."
            if len(dati_staz) > 0:
                # ordinamento dei dati in base a data e ora
                dati_staz_sorted = sorted(
                    dati_staz.items(),
                    key=lambda v: int(v[0].split("#")[5]),
                    reverse=True,
                )
                # assegnazione dei valori alle variabili
                portata = str(dati_staz_sorted[0][1])
                portata_6 = str(dati_staz_sorted[6][1])
            # formattazione dati
            if portata == "None" or portata_6 == "None":
                portata = "n.d."
                portata_6 = "n.d."
                tendenza6hprecedenti = "stazionario"
            elif (
                zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORTATA"
                or zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORT_FIU"
            ):
                portata_float = 0.0
                if portata != "n.d.":
                    portata_float = float(portata)
                portata_6_float = 0.0
                if portata_6 != "n.d.":
                    portata_6_float = float(portata_6)
                if portata_float > 0 and portata_6_float > 0:
                    obs = (float(portata) - float(portata_6)) / float(portata_6)
                else:
                    obs = 0
                if portata_float > 0:
                    portata = str(round(float(portata)))
                if portata_6_float > 0:
                    portata_6 = str(round(float(portata_6)))
                if obs < -0.1:
                    tendenza6hprecedenti = "diminuzione"
                elif obs >= -0.1 and obs <= 0.1:
                    tendenza6hprecedenti = "stazionario"
                elif obs >= 0.1:
                    tendenza6hprecedenti = "crescita"
            else:
                portata_float = 0.0
                if portata != "n.d.":
                    portata_float = float(portata)
                portata_6_float = 0.0
                if portata_6 != "n.d.":
                    portata_6_float = float(portata_6)
                if portata_float > 0 and portata_6_float > 0:
                    obs = (float(portata) - float(portata_6)) / float(portata_6)
                else:
                    obs = 0
                if portata_float > 0:
                    portata = str(round(float(portata), 2))
                if portata_6_float > 0:
                    portata_6 = str(round(float(portata_6), 2))
                if obs < -0.1:
                    tendenza6hprecedenti = "diminuzione"
                elif obs >= -0.1 and obs <= 0.1:
                    tendenza6hprecedenti = "stazionario"
                elif obs >= 0.1:
                    tendenza6hprecedenti = "crescita"

            if liv_1 == "n.d.":
                liv_1 = "n.d."
            elif (
                zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORTATA"
                or zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORT_FIU"
            ):
                liv_1 = round(liv_1)  # type: ignore
                if massimo_valore == "n.d.":
                    massimo_valore = "n.d."
                else:
                    massimo_valore = str(round(float(massimo_valore)))
            else:
                liv_1 = round(liv_1, 2)  # type: ignore
                massimo_valore = str(round(float(massimo_valore), 2))
            if massimo_data is None:
                massimo_data = "n.d."
            # else:
            #     massimo_data = datetime.datetime.strptime(
            #         massimo_data, "%Y-%m-%d"
            #     ).strftime("%d/%m/%Y")

            if liv_2 == "n.d.":
                liv_2 = "n.d."
            elif (
                zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORTATA"
                or zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORT_FIU"
            ):
                liv_2 = round(liv_2)  # type: ignore
                if massimo_valore == "n.d.":
                    massimo_valore = "n.d."
                else:
                    massimo_valore = str(round(float(massimo_valore)))
            else:
                liv_2 = round(liv_2, 2)  # type: ignore
                massimo_valore = str(round(float(massimo_valore), 2))
            if massimo_data is None:
                massimo_data = "n.d."
            # else:
            #     massimo_data = datetime.datetime.strptime(
            #         massimo_data, "%Y-%m-%d"
            #     ).strftime("%d/%m/%Y")

            if liv_3 == "n.d.":
                liv_3 = "n.d."
            elif (
                zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORTATA"
                or zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro
                == "PORT_FIU"
            ):
                liv_3 = round(liv_3)  # type: ignore
                if massimo_valore == "n.d.":
                    massimo_valore = "n.d."
                else:
                    massimo_valore = str(round(float(massimo_valore)))
            else:
                liv_3 = round(liv_3, 2)  # type: ignore
                massimo_valore = str(round(float(massimo_valore), 2))
            if massimo_data is None:
                massimo_data = "n.d."
            # else:
            #     massimo_data = datetime.datetime.strptime(
            #         massimo_data, "%Y-%m-%d"
            #     ).strftime("%d/%m/%Y")

            # Creazione criticità attesa
            max_critita_attesa = 0
            if portata == "n.d.":
                criticita_att = "A"
                max_critita_attesa = 0
            elif liv_1 == "n.d." or liv_2 == "n.d." or liv_3 == "n.d.":
                criticita_att = "A"
                max_critita_attesa = 0
            elif float(portata) >= float(liv_3):  # type: ignore
                criticita_att = "E"
                max_critita_attesa = 3
            elif float(portata) >= float(liv_1) and float(portata) < float(liv_2):  # type: ignore
                criticita_att = "O"
                max_critita_attesa = 1
            elif float(portata) >= float(liv_2) and float(portata) < float(liv_3):  # type: ignore
                criticita_att = "M"
                max_critita_attesa = 2
            else:
                criticita_att = "A"
                max_critita_attesa = 0
            # fine creazione criticità attesa
            maxvalore12 = float(maxvalore12)
            maxvalore24 = float(maxvalore24)
            maxvalore36 = float(maxvalore36)
            # Nel caso dell lago traslazione dello 0 idrometrico (-190)
            if zone_dict[str(w22_data_config[w]["id_w22_zone"])].id_parametro == "IDRO":
                maxvalore12 = maxvalore12 - float(190.0)
                maxvalore24 = maxvalore24 - float(190.0)
                maxvalore36 = maxvalore36 - float(190.0)
            # Creazione criticità 12 h
            max_critita_12h = 0
            if maxvalore12 == float(0):
                prev_crit12h = "A"
                max_critita_12h = 0
            elif liv_1 == "n.d." or liv_2 == "n.d." or liv_3 == "n.d.":
                prev_crit12h = "A"
                max_critita_12h = 0
            elif maxvalore12 >= float(liv_3):  # type: ignore
                prev_crit12h = "E"
                max_critita_12h = 3
            elif maxvalore12 >= float(liv_1) and maxvalore12 < float(liv_2):  # type: ignore
                prev_crit12h = "O"
                max_critita_12h = 1
            elif maxvalore12 >= float(liv_2) and maxvalore12 < float(liv_3):  # type: ignore
                prev_crit12h = "M"
                max_critita_12h = 2
            else:
                prev_crit12h = "A"
                max_critita_12h = 0
            # fine creazione criticità 12 h
            # Creazione criticità 24 h
            max_critita_24h = 0
            if maxvalore24 == 0:
                prev_crit24h = "A"
                max_critita_24h = 0
            elif liv_1 == "n.d." or liv_2 == "n.d." or liv_3 == "n.d.":
                prev_crit24h = "A"
                max_critita_24h = 0
            elif maxvalore24 >= float(liv_3):  # type: ignore
                prev_crit24h = "E"
                max_critita_24h = 3
            elif maxvalore24 >= float(liv_1) and maxvalore24 < float(liv_2):  # type: ignore
                prev_crit24h = "O"
                max_critita_24h = 1
            elif maxvalore24 >= float(liv_2) and maxvalore24 < float(liv_3):  # type: ignore
                prev_crit24h = "M"
                max_critita_24h = 2
            else:
                prev_crit24h = "A"
                max_critita_24h = 0
            # fine creazione criticità 24 h
            # Creazione criticità 36 h
            max_critita_36h = 0
            if maxvalore36 == 0:
                prev_crit36h = "A"
                max_critita_36h = 0
            elif liv_1 == "n.d." or liv_2 == "n.d." or liv_3 == "n.d.":
                prev_crit36h = "A"
                max_critita_36h = 0
            elif maxvalore36 >= float(liv_3):  # type: ignore
                prev_crit36h = "E"
                max_critita_36h = 3
            elif maxvalore36 >= float(liv_1) and maxvalore36 < float(liv_2):  # type: ignore
                prev_crit36h = "O"
                max_critita_36h = 1
            elif maxvalore36 >= float(liv_2) and maxvalore36 < float(liv_3):  # type: ignore
                prev_crit36h = "M"
                max_critita_36h = 2
            else:
                prev_crit36h = "A"
                max_critita_36h = 0
            # fine creazione criticità 36 h
            massimo_previsione_num = 0
            if max_critita_attesa > massimo_previsione_num:
                massimo_previsione_num = max_critita_attesa
            if max_critita_12h > massimo_previsione_num:
                massimo_previsione_num = max_critita_12h
            if max_critita_24h > massimo_previsione_num:
                massimo_previsione_num = max_critita_24h
            if max_critita_36h > massimo_previsione_num:
                massimo_previsione_num = max_critita_36h
            massimo_previsione = "X"
            if massimo_previsione_num == 0:
                massimo_previsione = "A"
            if massimo_previsione_num == 1:
                massimo_previsione = "O"
            if massimo_previsione_num == 2:
                massimo_previsione = "M"
            if massimo_previsione_num == 3:
                massimo_previsione = "E"
            w22_data_new_dict[w22_data_config[w]["id_w22_zone"]] = models.W22Data(
                id_w22=new,
                id_w22_zone=zone_dict[str(w22_data_config[w]["id_w22_zone"])],
                codice1=liv_1,
                codice2=liv_2,
                codice3=liv_3,
                tendenza6hprecedenti=tendenza6hprecedenti,
                portata_attesa=portata,
                criticita_attesa=criticita_att,
                prev_crit12h=prev_crit12h,
                prev_crit24h=prev_crit24h,
                prev_crit36h=prev_crit36h,
                tend48h=w22_data_config[w]["tend48h"],
                massimo_previsione=massimo_previsione,
                data_massimo_storico=massimo_data,
                valore_massimo_storico=massimo_valore,
            )
            # da assegnare
            # print(valore_modello)

        fine = datetime.datetime.now()
        print(
            "inizio salvataggioin w22_data ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        w22_data_list = []
        for w in w22_data_new_dict:
            w22_data_list.append(w22_data_new_dict[w])
        models.W22Data.objects.bulk_create(w22_data_list)
        fine = datetime.datetime.now()
        print(
            "new finito in ",
            abs((fine - inizio).total_seconds()),
            "secondi",
        )
        return Response({"id_w22": new.id_w22})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w22/bulletins/bulk_update/")
        print("========== user = ", request.user)
        print("========== request data = ", request.data)
        updated = 0
        snapshots = request.data
        id_w22 = snapshots["id_w22"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w22 = models.W22.objects.get(pk=id_w22)
        for snapshot in snapshots:
            setattr(w22, snapshot, snapshots[snapshot])
        w22.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W22SerializerFull(w22, context={"request": request})
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


class W22TendenzaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Tendenza to be viewed
    """

    queryset = models.W22Tendenza.objects.all()
    serializer_class = W22TendenzaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W22CriticitaView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Criticità to be viewed
    """

    queryset = models.W22Criticita.objects.all()
    serializer_class = W22CriticitaSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W22DataView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Data to be viewed or edited
    """

    queryset = models.W22Data.objects.all()
    serializer_class = W22DataSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def retrieve(self, request, pk=None):
        queryset = models.W22Data.objects
        w22Data = get_object_or_404(queryset, pk=pk)
        serializer = W22DataSerializer(w22Data, context={"request": request})
        return Response(serializer.data)


def convert_to_date(d, k):
    # TODO when support for Postgres 9.3 is dropped, remove the `replace` function call
    d[k] = datetime.datetime.strptime(
        d[k],
        "%Y-%m-%d",
    )


class W22ZoneView(viewsets.ModelViewSet):
    """
    API endpoint that allows W22 bulletin Zone to be viewed or edited
    """

    queryset = models.W22Zone.objects.all()
    serializer_class = W22ZoneSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class PieneComHtmlView(TemplateView):
    template_name = "piene_comunicazione.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W22.objects
        w22 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W22SerializerFull(w22)
        piene = serializer.data

        convert_to_date(piene, "data_validita")
        convert_to_date(piene, "data_emissione")

        context = {"piene": piene, "title": "Bollettino piene"}
        return context


class PieneComPDFView(PieneComHtmlView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="piene_comunicazione.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class PieneComPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        django_url = os.getenv("DJANGO_URL", "http://django:8000")
        r = requests.get(django_url + "/w22/comunicazione_pdf/%d" % kwargs["pk"])

        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(r.content)
            f.flush()
            png_name = "%s.png" % f.name
            command = "convert -verbose -density 145 -crop 900x1000+3x5 %s %s" % (
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


class PieneHTMLView(TemplateView):
    template_name = "piene.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W22.objects
        w22 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W22SerializerFull(w22)
        piene = serializer.data

        convert_to_date(piene, "data_validita")
        convert_to_date(piene, "data_emissione")

        context = {"piene": piene, "title": "Bollettino piene"}
        return context


class PienePDFView(PieneHTMLView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="piene.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class PienePngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        django_url = os.getenv("DJANGO_URL", "http://django:8000")
        r = requests.get(django_url + "/w22/pdf/%d" % kwargs["pk"])

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
    template_name = "piene.kml"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        queryset = models.W22.objects
        w22 = get_object_or_404(queryset, pk=kwargs["pk"])
        serializer = W22SerializerFull(w22)
        piene = serializer.data
        data_piene = datetime.datetime.strptime(
            str(piene["data_emissione"]), "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        convert_to_date(piene, "data_validita")
        convert_to_date(piene, "data_emissione")

        context = {
            "piene": piene,
            "data_piene": data_piene,
            "title": "Bollettino piene",
        }
        return context
