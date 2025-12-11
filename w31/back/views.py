#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

import datetime
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
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from wkhtmltopdf.views import PDFTemplateResponse

from w31.back import models
from w31.back.fwi import FWIClass
from w31.back.serializers import (
    W31DataMacroareeLivelliSerializer,
    W31LivelliSerializer,
    W31MacroareeInputSerializer,
    W31Serializer,
    W31SerializerFull,
)
from website.common.tasks import send_with_celery
from website.common.views import BulletinDraftLocked, StandardResultsSetPagination


def first_guess(username, start, draft=0):
    print("start =", start)

    now = datetime.datetime.now()
    start = datetime.datetime.combine(
        start, datetime.datetime.min.time()
    )  # porto start alle 00:00
    emissione = start.replace(hour=12, minute=00, second=0, microsecond=0)
    next_blt_time = emissione + datetime.timedelta(days=1)

    agls = models.W31AreeGiorniLivelli.objects.all()

    parametro_terma = models.Parametro.objects.get(id_parametro="TERMA")
    parametro_igro = models.Parametro.objects.get(id_parametro="IGRO")
    parametro_velv = models.Parametro.objects.get(id_parametro="VELV")
    parametro_cum_pluv = models.Parametro.objects.get(id_parametro="CUM_PLUV")
    parametro_ffmc = models.Parametro.objects.get(id_parametro="FFMC_INDEX")
    parametro_dmc = models.Parametro.objects.get(id_parametro="DMC_INDEX")
    parametro_dc = models.Parametro.objects.get(id_parametro="DC_INDEX")
    parametro_isi = models.Parametro.objects.get(id_parametro="ISI_INDEX")
    parametro_bui = models.Parametro.objects.get(id_parametro="BUI_INDEX")
    parametro_fwi = models.Parametro.objects.get(id_parametro="FWI_INDEX")
    ffmc = ffmc0 = 85.0  # Valore harcodato del giorno prima
    dmc = dmc0 = 6.0  # Valore harcodato del giorno prima
    dc = dc0 = 15.0  # Valore harcodato del giorno prima

    # today è l'oggi vero
    today = datetime.datetime.today()
    today = datetime.datetime.combine(
        today, datetime.datetime.min.time()
    )  # porto today alle 00:00

    # days_offset è quanti giorni rispetto a today sto facendo il bollettino
    days_offset = (today - start).days

    # range di giorni necessari per fare le previsioni
    tl_min = 49 - 17 * days_offset
    tl_max = 49 + 17 * 8 - 17 * days_offset

    rolling = {}
    # filtro la vista rolling e sort per microaree e timelayouts perchè devono essere ciclati
    rolling_qs = models.W31Rolling.objects.filter(
        id_time_layouts__range=(tl_min, tl_max)
    ).order_by("id_w31_microaree", "id_time_layouts")

    id = 1
    if rolling_qs.count() == 0:
        # crea i dati se la w31input è vuota
        for id_tl in [49, 66, 83, 100, 117, 134, 151, 168, 185]:
            for microarea in models.W31Microaree.objects.all():
                rolling[id] = models.W31Rolling(
                    id=id,
                    temp=-9999,
                    umid=-9999,
                    velv=-9999,
                    prec=-9999,
                    id_w31_microaree=microarea,
                    id_time_layouts=id_tl,
                )
                id = id + 1
    else:
        for roll_rec in rolling_qs:
            rolling[roll_rec.id] = models.W31Rolling(
                id=roll_rec.id,
                temp=roll_rec.temp,
                umid=roll_rec.umid,
                velv=roll_rec.velv,
                prec=roll_rec.prec,
                id_w31_microaree=roll_rec.id_w31_microaree,
                id_time_layouts=roll_rec.id_time_layouts,
            )

    yesterday_fwi = {}
    yesterday = start - datetime.timedelta(days=1)
    olds = (
        models.W31.objects.filter(start_valid_time__date=yesterday)
        .filter(status="1")
        .order_by("-last_update")
    )
    if len(olds) == 0:
        microaree = models.W31Microaree.objects.all()
        for microarea in microaree:
            yesterday_fwi[microarea.id_w31_microaree] = {
                "ffmc": ffmc0,
                "dmc": dmc0,
                "dc": dc0,
            }
        print("new(): Primo bollettino imposto il sequenziale a 1")
        new_seq = 1
    else:
        old = olds.latest("pk")
        # gestione anno nuovo
        if old.start_valid_time.year < start.year:
            print("new(): cambio dell'anno imposto il sequenziale a 1")
            new_seq = 1
        else:
            old_seq_num = old.seq_num if old.seq_num is not None else 0
            new_seq = old_seq_num + 1
        old_data = models.W31DataMicroareeLivelli.objects.filter(
            id_w31=old.id_w31, id_time_layouts=49
        )  # 47 records
        for od in old_data:
            old_parameters = models.W31DataMicroareeParametri.objects.filter(
                id_w31_data_microaree_livelli=od.id_w31_data_microaree_livelli
            )  # 10 records
            ffmc = old_parameters.get(id_parametro=parametro_ffmc).numeric_value
            print(
                od.id_w31_microaree,
                od.id_time_layouts,
                " old_parameters.get(id_parametro=parametro_ffmc).numeric_value",
                old_parameters.get(id_parametro=parametro_ffmc).numeric_value,
            )
            dmc = old_parameters.get(id_parametro=parametro_dmc).numeric_value
            print(
                od.id_w31_microaree,
                od.id_time_layouts,
                " old_parameters.get(id_parametro=parametro_dmc).numeric_value",
                old_parameters.get(id_parametro=parametro_dmc).numeric_value,
            )
            dc = old_parameters.get(id_parametro=parametro_dc).numeric_value
            print(
                od.id_w31_microaree,
                od.id_time_layouts,
                " old_parameters.get(id_parametro=parametro_dc).numeric_value",
                old_parameters.get(id_parametro=parametro_dc).numeric_value,
            )
            yesterday_fwi[od.id_w31_microaree.id_w31_microaree] = {
                "ffmc": ffmc,
                "dmc": dmc,
                "dc": dc,
            }

    # creazione nuovo bollettino
    new_w31 = models.W31(
        start_valid_time=emissione,
        validity=72,
        next_blt_time=next_blt_time,
        status=draft,  # il nuovo bollettino lo metto in bozza, draft = True
        last_update=now,
        username=username,
        seq_num=new_seq,  # incremento il sequenziale,
        version=0,
        algoritmo="py",
        id_w31_parent=None,
        annotazione="-",
    )
    new_w31.save()

    # 2024-08-30
    # le condizioni iniziali vengono prese dall'ultimo bollettino valida con id_time_layout = 49
    # altrimenti ci sonod dei valori iniziali di default che sono poco realistici
    # l'alimentatore di w31_input sostituisce i valori iniziali nella tabella
    # public.w31_data_microaree_parametri con un update dat w31_input_valori_iniziali

    for rec_id in rolling:
        record = rolling[rec_id]
        corrected_id_time_layout = record.id_time_layouts + 17 * days_offset

        if corrected_id_time_layout == 49:  # timelayout che indicata la giornata oggi
            ffmc0 = yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["ffmc"]
            print(
                'timelayout 49 yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["ffmc"]',
                yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["ffmc"],
            )
            dmc0 = yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["dmc"]
            print(
                'timelayout 49 yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["dmc"]',
                yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["dmc"],
            )
            dc0 = yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["dc"]
            print(
                'timelayout 49 yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["dc"]',
                yesterday_fwi[record.id_w31_microaree.id_w31_microaree]["dc"],
            )
            mth = start.month

        else:  # per gli altri timelayouts ovvero i giorni futuri delle previsioni
            # uso i dati del giorno prima per calcolare le variabili intermedie
            ffmc0 = ffmc  # Valore del giorno prima
            dmc0 = dmc  # Valore del giorno prima
            dc0 = dc  # Valore del giorno prima

        print(
            record.id_w31_microaree,
            record.id_time_layouts,
            record.temp,
            record.umid,
            record.velv,
            record.prec,
            "mth",
            mth,
            "ffmc0",
            ffmc0,
            "dmc0",
            dmc0,
            "dc0",
            dc0,
        )
        if (
            record.temp != -9999
            and record.umid != -9999
            and record.velv != -9999
            and record.prec != -9999
        ):
            fwisystem = FWIClass(record.temp, record.umid, record.velv, record.prec)
            ffmc = fwisystem.FFMCcalc(ffmc0)
            dmc = fwisystem.DMCcalc(dmc0, mth)
            dc = fwisystem.DCcalc(dc0, mth)
            isi = fwisystem.ISIcalc(ffmc)
            bui = fwisystem.BUIcalc(dmc, dc)
            fwi = fwisystem.FWIcalc(isi, bui)
        else:
            ffmc = -9999
            dmc = -9999
            dc = -9999
            isi = -9999
            bui = -9999
            fwi = -9999

        giorno = min(
            int((start + datetime.timedelta(days=days_offset)).strftime("%j")), 365
        )  # giorno dell'anno + il day_offset (se bisestile si riusa il 365 giorno, hanno stesse soglie)

        # prendo la microarea del mio record
        mi = record.id_w31_microaree
        # filtro la tabella AreeGiorniLivelli per i due parametri che ho per ridurla
        agls_filtrati = agls.filter(
            id_w31_giorni=giorno, id_w31_microaree=mi.id_w31_microaree
        ).order_by("soglia_superiore")

        # ciclo queryset per confronto soglie e fwi
        if fwi != -9999:
            livello = None
            for agl in agls_filtrati:
                soglia_superiore = agl.soglia_superiore
                if (
                    fwi <= soglia_superiore
                ):  # se fwi è più piccolo della soglia, essendo ordinate ho il livello e posso uscire dal loop
                    livello = agl.id_w31_livelli
                    break
                else:
                    pass

            if livello is None:  # se è True: fwi > 21.3
                livello = models.W31Livelli.objects.get(id_w31_livelli=5)  # livello 5
        else:
            livello = models.W31Livelli.objects.get(
                id_w31_livelli=-9999
            )  # livello -9999

        # trasformo corrected_id_time_layout in una vera istanza del modello TimeLayouts
        tl_instance = models.TimeLayouts.objects.get(
            id_time_layouts=corrected_id_time_layout
        )

        # inserisco valori nella tabella data_microaree_livelli
        new_data_microaree_livelli = models.W31DataMicroareeLivelli(
            id_w31=new_w31,
            id_w31_microaree=mi,
            id_w31_livelli=livello,
            id_time_layouts=tl_instance,
        )
        # print("---- inserisco W31DataMicroareeLivelli", new_w31, mi, livello, tl_instance)
        new_data_microaree_livelli.save()

        # inserisco valori nella tabella data_parametri, per i 10 parametri diversi

        # TERMA
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_terma,
            numeric_value=record.temp,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_terma, record.temp)
        new_data_microcaree_parametri.save()

        # IGRO
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_igro,
            numeric_value=record.umid,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_igro, record.umid)
        new_data_microcaree_parametri.save()

        # VELV
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_velv,
            numeric_value=record.velv,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_velv, record.velv)
        new_data_microcaree_parametri.save()

        # CUM_PLUV
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_cum_pluv,
            numeric_value=record.prec,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_cum_pluv, record.prec)
        new_data_microcaree_parametri.save()

        # FFMC_INDEX
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_ffmc,
            numeric_value=ffmc,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_ffmc, ffmc)
        new_data_microcaree_parametri.save()

        # DMC_INDEX
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_dmc,
            numeric_value=dmc,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_dmc, dmc)
        new_data_microcaree_parametri.save()

        # DC_INDEX
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_dc,
            numeric_value=dc,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_dc, dc)
        new_data_microcaree_parametri.save()

        # ISI_INDEX
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_isi,
            numeric_value=isi,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_isi, isi)
        new_data_microcaree_parametri.save()

        # BUI_INDEX
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_bui,
            numeric_value=bui,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_bui, bui)
        new_data_microcaree_parametri.save()

        # FWI_INDEX
        new_data_microcaree_parametri = models.W31DataMicroareeParametri(
            id_w31_data_microaree_livelli=new_data_microaree_livelli,
            id_parametro=parametro_fwi,
            numeric_value=fwi,
        )
        # print("---- inserisco W31DataMicroareeParametri", new_data_microaree_livelli, parametro_fwi, fwi)
        new_data_microcaree_parametri.save()

    # calcolo della first guess per le macroaree

    Ma = models.W31Macroaree.objects.all()
    mMa = models.W31MicroMacroAree.objects.all()
    dml = models.W31DataMicroareeLivelli.objects.all()

    # prendere solo colonna id_time_layouts da rolling
    tls = []
    if rolling_qs.count() > 0:
        for id_tl in rolling_qs.order_by("id_time_layouts").distinct("id_time_layouts"):  # type: ignore
            tls.append(id_tl.id_time_layouts)  # type: ignore
    else:
        tls = [49, 66, 83, 100, 117, 134, 151, 168, 185]

    for ma in Ma:
        aree_giuste = mMa.filter(
            id_w31_macroaree=ma.id_w31_macroaree
        )  # (è un QuerySet) prendere l'elenco delle microaree contenute nelle macroaree corrente

        aree_aggiustate = [
            item.id_w31_microaree for item in aree_giuste
        ]  # rigiro aree_giuste in modo che sia istantza di W31Microaree e non di W31MicroMacroaree

        lista_ettari_forestali = []
        for x in aree_aggiustate:
            lista_ettari_forestali.append(
                x.ettari_forestali
            )  # lista py dei valori degli ettari delle micro per una macro

        for tl in tls:
            corrected_id_time_layout = tl + 17 * days_offset

            temp = dml.filter(
                id_time_layouts_id=corrected_id_time_layout,
                id_w31_microaree__in=aree_aggiustate,
                id_w31=new_w31,
            )  # prendere i livelli di tutte le microaree contenute nella macroarea corrente con uguale TL

            # estrarre i livelli da temp e fare aggregazione

            lvl = [item.id_w31_livelli for item in temp]

            # Per calcolare la media pesata
            # fare la somma tra i prodotti di ciascun numero per il corrispondente peso,
            # poi dividere per la somma dei pesi

            somma_prodotti = 0.0
            for q in range(len(lista_ettari_forestali)):
                somma_prodotti = (
                    somma_prodotti + lvl[q].id_w31_livelli * lista_ettari_forestali[q]
                )

            media_ponderata = round(
                somma_prodotti / sum(lista_ettari_forestali)
            )  # aka livello macroarea

            livello = models.W31Livelli.objects.get(pk=media_ponderata)

            # trasformo corrected_id_time_layout in una vera istanza del modello TimeLayouts
            tl_instance = models.TimeLayouts.objects.get(
                id_time_layouts=corrected_id_time_layout
            )

            new_data_macroaree_livelli = models.W31DataMacroareeLivelli(
                id_w31=new_w31,
                id_w31_macroaree=ma,  # ma è già l'id della macroarea
                id_w31_livelli=livello,
                id_time_layouts=tl_instance,
                wind="N",
            )
            # print("---- inserisco W31DataMacroareeLivelli", new_w31, ma, livello, tl_instance, "N")
            new_data_macroaree_livelli.save()

    return new_w31


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class W31View(viewsets.ModelViewSet):
    """
    API endpoint that allows W31 bulletins to be viewed or edited
    """

    queryset = models.W31.objects.order_by("-last_update", "-seq_num", "-pk")
    serializer_class = W31Serializer
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
        queryset = models.W31.objects
        if (
            instance.id_w31_parent
            and queryset.filter(pk=instance.id_w31_parent).exists()
        ):
            w31 = get_object_or_404(queryset, pk=instance.id_w31_parent)
            w31.status = "1"
            if not User.objects.filter(username=w31.username).exists():
                print("perform_destroy non trovo l'utente " + w31.username)
                w31.username = (
                    instance.username
                )  # se rimane l'utente originale post_save potrebbe
                # generare errore se non trova l'utente originale in auth_user
            w31.save()
        instance.delete()

    def retrieve(self, request, pk=None):
        queryset = models.W31.objects
        w31 = get_object_or_404(queryset, pk=pk)
        serializer = W31SerializerFull(w31, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def new(self, request):
        print("INIZIO AZIONE NEW")

        start = datetime.datetime.today()
        username = request.user

        new_w31 = first_guess(username, start)

        return Response({"id_w31": new_w31.id_w31})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def reopen(self, request, pk):
        # riapre un bollettino
        now = datetime.datetime.now()
        old = models.W31.objects.get(pk=pk)
        print("w31 reopen:", old)
        old.status = "2"
        old_id_w31 = old.id_w31
        old.save()
        old_seq_num = old.seq_num if old.seq_num is not None else 0
        new_seq = old_seq_num + 1
        # anno = int(old.seq_num)
        new = old
        new.pk = None  # resetta la chiave primaria rendendolo un nuovo record
        new.status = "0"
        new.seq_num = new_seq
        new.last_update = now
        new.username = request.user
        new.id_w31_parent = old_id_w31
        new.save()
        # Dati MicroAree
        old_dataMiL = models.W31DataMicroareeLivelli.objects.filter(id_w31=old_id_w31)
        for odmil in old_dataMiL:
            data_id_w31_data_microaree_livelli = odmil.id_w31_data_microaree_livelli
            ndmil = odmil
            ndmil.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            ndmil.id_w31 = new
            ndmil.save()
            old_dataMiP = models.W31DataMicroareeParametri.objects.filter(
                id_w31_data_microaree_livelli=data_id_w31_data_microaree_livelli
            )
            for odmip in old_dataMiP:
                ndmip = odmip
                ndmip.pk = None
                ndmip.id_w31_data_microaree_livelli = ndmil
                ndmip.save()
        # Dati MacroAree
        old_dataMaL = models.W31DataMacroareeLivelli.objects.filter(id_w31=old_id_w31)
        for odmal in old_dataMaL:
            data_id_w31_data_macroaree_livelli = odmal.id_w31_data_macroaree_livelli
            ndmal = odmal
            ndmal.pk = None  # resetta la chiave primaria rendendolo un nuovo record
            ndmal.id_w31 = new
            ndmal.save()
            old_dataMaP = models.W31DataMacroareeParametri.objects.filter(
                id_w31_data_macroaree_livelli=data_id_w31_data_macroaree_livelli
            )
            for odmap in old_dataMaP:
                ndmap = odmap
                ndmap.pk = None
                ndmap.id_w31_data_macroaree_livelli = ndmal
                ndmap.save()
        return Response({"id_w31": new.id_w31})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def copy(self, request, pk):
        # TBD
        return Response({"id_w31": 1})

    @action(detail=True, permission_classes=[permissions.IsAuthenticated])
    @atomic
    def send(self, request, pk):
        inizio = datetime.datetime.now()
        w31 = models.W31.objects.get(pk=pk)
        w31.status = "1"
        w31.username = request.user.username
        w31.last_update = inizio
        w31.save()
        fine = datetime.datetime.now()
        print("send finito in ", abs((fine - inizio).total_seconds()), "secondi")
        send_with_celery("incendi", w31.id_w31)
        return Response({"id_w31": w31.id_w31})

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    @atomic
    def bulk_update(self, request):
        inizio = datetime.datetime.now()
        print("========== POST /w31/bulletins/bulk_update/")
        print("========== user = ", self.request.user)
        print("========== request data = ", self.request.data)
        updated = 0
        snapshots = self.request.data
        id_w31 = snapshots["id_w31"]
        last_update = datetime.datetime.now()
        snapshots["last_update"] = last_update
        w31 = models.W31.objects.get(pk=id_w31)
        for snapshot in snapshots:
            setattr(w31, snapshot, snapshots[snapshot])
        w31.save()
        updated += 1
        fine = datetime.datetime.now()
        serializer = W31SerializerFull(w31, context={"request": request})
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


class W31CurrentView(RetrieveAPIView):
    """
    View the latest W31 bulletin sent
    """

    queryset = models.W31.objects.filter(status="1").order_by("-last_update")
    serializer_class = W31SerializerFull
    lookup_field = "start_valid_time__date"
    lookup_url_kwarg = "emissione"


class W31DataMacroareeLivelliView(viewsets.ModelViewSet):
    """
    API endpoint that allows W31 bulletin Data to be viewed or updated
    """

    queryset = models.W31DataMacroareeLivelli.objects.all()
    serializer_class = W31DataMacroareeLivelliSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


class W31LivelliView(viewsets.ModelViewSet):
    """
    API endpoint that allows W31 levels to be viewed
    """

    queryset = models.W31Livelli.objects.all()
    serializer_class = W31LivelliSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]


def convert_to_datetime(d, k):
    d[k] = datetime.datetime.strptime(
        d[k].split(".")[0],
        "%Y-%m-%dT%H:%M:%S",
    )


class IncendiSVGView(TemplateView):
    template_name = "incendi.svg"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs):
        w31 = get_object_or_404(models.W31.objects, pk=kwargs["pk"])
        serializer = W31SerializerFull(w31)
        incendi = serializer.data

        tabella_vento = {}  # type: ignore

        for i in incendi["w31datamacroareelivelli_set"]:
            tabella_vento[i["id_w31_macroaree"]["id_w31_macroaree"]] = {}
        for i in incendi["w31datamacroareelivelli_set"]:
            tabella_vento[i["id_w31_macroaree"]["id_w31_macroaree"]][
                i["id_time_layouts"]
            ] = i["wind"]

        start = w31.start_valid_time.date()
        end = start + datetime.timedelta(days=6)

        inputs = {}

        mais = models.W31MacroareeInput.objects.filter(
            data__range=(start, end)
        ).order_by("id_w31_macroaree__ordine_bollettino", "data")
        for mai in mais:
            serializer = W31MacroareeInputSerializer(mai)
            inputs[mai] = serializer.data

        tabella_inputs = {}  # type: ignore

        for i in inputs:
            key = i.id_w31_macroaree.nome
            if key not in tabella_inputs:
                tabella_inputs[key] = []
            tabella_inputs[key].append(i.data.strftime("%y-%m-%d"))
            tabella_inputs[key].append(i.prec)
            tabella_inputs[key].append(i.ws)
            tabella_inputs[key].append(i.rh)
            tabella_inputs[key].append(i.deltat)
        convert_to_datetime(incendi, "next_blt_time")
        convert_to_datetime(incendi, "start_valid_time")

        tabella_incendi = {}  # type: ignore

        for dmal in incendi["w31datamacroareelivelli_set"]:
            key = dmal["id_w31_macroaree"]["nome"]
            if key not in tabella_incendi:
                tabella_incendi[key] = []
            tabella_incendi[key].append(dmal["id_w31_livelli"])

        # sort tabella by ordine_bollettino
        ordine_bollettino = models.W31Macroaree.objects.values_list(
            "nome", flat=True
        ).order_by("ordine_bollettino")
        tabella_incendi = {key: tabella_incendi[key] for key in ordine_bollettino}

        for k, v in tabella_incendi.items():  # ciclo chiavi/valori della tabella
            div = len(v) - 3  # conto il numero di elementi dopo il terzo
            total = sum(x for x in v[3:])  # li sommo
            v = v[:4]  # riassegno solo i primi 4 elementi del valore
            v.append(
                int((total / div - v[2]) * 5)
            )  # aggiungo il valore della classe tendenza come la media dei valori dopo il terzo,
            # utilizzando 5 come fattore di amplificazione
            tabella_incendi[k] = v  # riassegno come valore della chiave il nuovo array

        today = incendi["start_valid_time"]
        tomorrow = incendi["start_valid_time"] + datetime.timedelta(days=1)
        tdat = incendi["start_valid_time"] + datetime.timedelta(days=2)
        day4 = incendi["start_valid_time"] + datetime.timedelta(days=3)
        day5 = incendi["start_valid_time"] + datetime.timedelta(days=4)
        day6 = incendi["start_valid_time"] + datetime.timedelta(days=5)
        day7 = incendi["start_valid_time"] + datetime.timedelta(days=6)

        # prendo colori livelli dal db
        livelli = {}
        queryset = models.W31Livelli.objects.all()
        for liv in queryset:
            serializer = W31LivelliSerializer(liv)
            livelli[liv] = serializer.data

        context = {
            "inputs": inputs,
            "tabella_inputs": tabella_inputs,
            "incendi": incendi,
            "tabella_incendi": tabella_incendi,
            "dates": [today, tomorrow, tdat, day4, day5, day6, day7],
            "livelli": livelli,
            "tabella_vento": tabella_vento,
        }
        return context


class IncendiPDFView(IncendiSVGView):
    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        response = PDFTemplateResponse(
            request=request,
            template=self.template_name,
            context=self.get_context_data(**kwargs),
            filename="incendi.pdf",
            cmd_options={
                "margin-bottom": 0,
                "margin-left": 0,
                "margin-right": 0,
                "margin-top": 0,
            },
        )
        return response


class IncendiPngView(DetailView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        os.environ.pop("http_proxy", None)
        os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)
        django_url = os.getenv("DJANGO_URL", "http://django:8000")
        r = requests.get(django_url + "/w31/pdf/%d" % kwargs["pk"])

        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(r.content)
            f.flush()
            png_name = "%s.png" % f.name
            command = (
                "convert -verbose -density 145 -crop 1191x1685+3x5 %s -append %s"
                % (
                    f.name,
                    png_name,
                )
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
