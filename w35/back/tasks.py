#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#
import datetime
import logging
import time
from collections import deque

from django.db import connection

from config import celery_app
from w35.back import models
from website.core import models as models_w05

log = logging.getLogger(__name__)


@celery_app.task(soft_time_limit=1200, time_limit=1200)
def save_comuni(id_w35, username):
    print("========== save_comuni")
    inizio = datetime.datetime.now()
    # try:
    now = datetime.datetime.now()

    time_layouts = models.TimeLayouts.objects.all()
    time_layouts_dict = {}
    for mm in time_layouts:
        time_layouts_dict[mm.id_time_layouts] = mm

    sky_conditions = models.SkyCondition.objects.all()
    sky_conditions_dict = {}
    for mmm in sky_conditions:
        sky_conditions_dict[mmm.id_sky_condition] = mmm

    wind_class = models.WindClass.objects.all()
    wind_class_dict = {}
    for mmmm in wind_class:
        wind_class_dict[mmmm.code] = mmmm

    parametro = models.Parametro.objects.all().select_related("id_unita_misura")
    parametro_dict = {}
    for mmmmm in parametro:
        parametro_dict[mmmmm.id_parametro] = mmmmm

    stazioni_rappresentative_comune = models.StazioniRappresentativeComune.objects.all()
    stazioni_rappresentative_comune_dict = {}
    for mmmmmm in stazioni_rappresentative_comune:
        stazioni_rappresentative_comune_dict[mmmmmm.id_comune] = mmmmmm

    tls_pomeriggio = [48, 65, 82, 99]
    tls_mattino = [64, 81, 98]

    tls = tls_mattino + tls_pomeriggio

    bulletin = models.W35.objects.filter(id_w35=id_w35).get()
    # rel_aree_meteo_comune = models.RelAreeMeteoComune.objects.filter(id_area_meteo="MET-1")
    rel_aree_meteo_comune = models.RelAreeMeteoComune.objects.all()

    forecast_comuni_array = []

    print("inizio append in memoria")
    for tl in tls:
        for rel in rel_aree_meteo_comune:
            bulletin_data = (
                models.W35Data.objects.filter(id_w35=id_w35)
                .filter(id_time_layouts=tl)
                .filter(id_area_meteo=rel.id_area_meteo)
            )
            bulletin_sky_condition = 0
            bulletin_freezing_level = 0
            bulletin_snow_level = 0
            for data in bulletin_data:
                if data.id_parametro == parametro_dict["SKY_12"]:
                    bulletin_sky_condition = data.numeric_value  # type: ignore
                if data.id_parametro == parametro_dict["ZERO"]:
                    bulletin_freezing_level = data.numeric_value  # type: ignore
                if data.id_parametro == parametro_dict["SNOW_LEV"]:
                    bulletin_snow_level = data.numeric_value  # type: ignore

            start_time = str(time_layouts_dict[tl].start_time)[0:5]
            start_day_offset = time_layouts_dict[tl].start_day_offset
            start_date = (
                bulletin.data_emissione + datetime.timedelta(days=start_day_offset)
            ).strftime("%Y-%m-%d")

            end_time = str(time_layouts_dict[tl].start_time)[0:5]
            end_day_offset = time_layouts_dict[tl].start_day_offset
            end_date = (
                bulletin.data_emissione + datetime.timedelta(days=end_day_offset)
            ).strftime("%Y-%m-%d")
            # print(str(start_time) + " " + str(start_day_offset) + " " + str(start_date) + " "
            #   + str(end_time) + " " + str(end_day_offset) + " " + str(end_date))

            comune_staz = stazioni_rappresentative_comune_dict[rel.id_comune]

            if tl in tls_pomeriggio:
                query_tmax = (
                    models.WeatherQuery.objects.filter(id_query=1).get().sql_text
                )
                query_tmax = query_tmax.replace("#start_date#", start_date)  # type: ignore
                query_tmax = query_tmax.replace("#start_time#", start_time)
                query_tmax = query_tmax.replace("#end_date#", end_date)
                query_tmax = query_tmax.replace(
                    "#cod_staz_meteo#",
                    str(comune_staz.cod_staz_meteo_terma.cod_staz_meteo),
                )
                cursor = connection.cursor()
                cursor.execute(query_tmax)
                air_temperature = cursor.fetchone()
                if air_temperature is not None:
                    air_temperature = air_temperature[0]

            elif tl in tls_mattino:
                query_tmin = (
                    models.WeatherQuery.objects.filter(id_query=2).get().sql_text
                )
                query_tmin = query_tmin.replace("#start_date#", start_date)  # type: ignore
                query_tmin = query_tmin.replace("#start_time#", start_time)
                query_tmin = query_tmin.replace("#end_date#", end_date)
                query_tmin = query_tmin.replace(
                    "#cod_staz_meteo#",
                    str(comune_staz.cod_staz_meteo_terma.cod_staz_meteo),
                )
                cursor = connection.cursor()
                cursor.execute(query_tmin)
                air_temperature = cursor.fetchone()
                if air_temperature is not None:
                    air_temperature = air_temperature[0]

            query_igro = models.WeatherQuery.objects.filter(id_query=39).get().sql_text
            query_igro = query_igro.replace("#start_date#", start_date)  # type: ignore
            query_igro = query_igro.replace("#start_time#", start_time)
            query_igro = query_igro.replace("#end_date#", end_date)
            query_igro = query_igro.replace("#end_time#", end_time)
            query_igro = query_igro.replace(
                "#cod_staz_meteo#", str(comune_staz.cod_staz_meteo_igro.cod_staz_meteo)
            )
            cursor = connection.cursor()
            cursor.execute(query_igro)
            humidity = cursor.fetchone()
            if humidity is not None:
                humidity = humidity[0]

            query_velv = models.WeatherQuery.objects.filter(id_query=6).get().sql_text
            query_velv = query_velv.replace("#start_date#", start_date)  # type: ignore
            query_velv = query_velv.replace("#start_time#", start_time)
            query_velv = query_velv.replace("#end_date#", end_date)
            query_velv = query_velv.replace("#end_time#", end_time)
            query_velv = query_velv.replace(
                "#cod_staz_meteo#", str(comune_staz.cod_staz_meteo_velv.cod_staz_meteo)
            )
            cursor = connection.cursor()
            cursor.execute(query_velv)
            wind_code = cursor.fetchone()
            if wind_code is not None:
                wind_code = wind_code[0]

            wind_direction = None
            query_dirv = models.WeatherQuery.objects.filter(id_query=48).get().sql_text
            query_dirv = query_dirv.replace("#start_date#", start_date)  # type: ignore
            query_dirv = query_dirv.replace("#start_time#", start_time)
            query_dirv = query_dirv.replace("#end_date#", end_date)
            query_dirv = query_dirv.replace("#end_time#", end_time)
            query_dirv = query_dirv.replace(
                "#cod_staz_meteo#", str(comune_staz.cod_staz_meteo_velv.cod_staz_meteo)
            )
            cursor = connection.cursor()
            cursor.execute(query_dirv)
            wind_direction = cursor.fetchone()
            if wind_direction is not None:
                wind_direction = wind_direction[0]

            start_time = datetime.datetime.strptime(  # type: ignore
                start_date + " " + str(time_layouts_dict[tl].start_time),
                "%Y-%m-%d %H:%M:%S",
            )
            end_time = datetime.datetime.strptime(  # type: ignore
                end_date + " " + str(time_layouts_dict[tl].end_time),
                "%Y-%m-%d %H:%M:%S",
            )
            # print(str(start_time) + " " + str(end_time) + " " + str(bulletin.data_emissione))
            id_comune = rel.id_comune
            id_time_layouts = time_layouts_dict[tl]
            sky_condition = None
            if bulletin_sky_condition is not None:
                sky_condition = sky_conditions_dict[bulletin_sky_condition]
            new_forecast = models.ForecastComuni(
                id_comune=id_comune,
                data_emissione=bulletin.data_emissione,
                start_time=start_time,
                end_time=end_time,
                id_time_layouts=id_time_layouts,
                sky_condition=sky_condition,
                air_temperature=air_temperature,
                humidity=humidity,
                wind_class=wind_class_dict[wind_code],
                wind_direction=wind_direction,
                trend=None,
                snow_level=bulletin_freezing_level,
                freezing_level=bulletin_snow_level,
                last_update=now,
                username=username,
            )
            forecast_comuni_array.append(new_forecast)
            fine = datetime.datetime.now()
            # print("append " + str(id_comune.id_comune) + " " + str(start_time) + " " + str(end_time) +
            #     " " + str(id_time_layouts.id_time_layouts) + " " + str(abs((fine - inizio).total_seconds())) +
            #     " " + str(len(forecast_comuni_array)))
            # prendi lo sky condition, lo zero termico e la quota neve dell'area meteo da w35_data e
            # in base alla tabella rel_aree_meteo_comune salva in forecast_comuni

            # query_tmax CONSTANT INTEGER := 1;
            # query_tmin CONSTANT INTEGER := 2;
            # query_igro CONSTANT INTEGER := 39;
            # query_velv CONSTANT INTEGER := 6;
            # query_dirv CONSTANT INTEGER := 48;
            # time_array CONSTANT INTEGER ARRAY[8] := '{48, 64, 65, 81, 82, 98, 99}';

            # per la temperatura, l'umidità e la classe di vento esegui weather_query
            # per tutti i time_layouts
            #   per tutti i comuni
            #       cerca le stazioni rappresentative nella tabella stazioni_rappresentative_comune
            #           sulle tre stazioni trovate esegui le query dando in input alla query l'id_query
            #           lo start_date, start_time, end_date, end_time dal id_time_layouts quindi fai i replace
            #           nell'sql scritto in weather_query
            #   /* Direzione vento */
            #   SELECT INTO my_record_weather
            #      REPLACE (REPLACE (REPLACE (REPLACE (REPLACE (sql_text,
            #         '#cod_staz_meteo#', my_record_stazione.cod_staz_meteo_velv),
            #         '#start_date#', my_record_timestamp.start_d::TEXT),
            #         '#start_time#', my_record_timestamp.start_t::TEXT),
            #         '#end_date#', my_record_timestamp.end_d::TEXT),
            #         '#end_time#', my_record_timestamp.end_t::TEXT
            #         ) AS sql
            #   FROM weather_query
            #   WHERE id_query = query_dirv;
            # Person.objects.raw("SELECT id, first_name, last_name, birth_date FROM myapp_person")

            # correggi l'icona in base allo scarto tra quota neve e quota comune

            # sistema le classi di vento in caso di skycondition con vento

            # salva su forecast_comuni
    # except Exception as e:
    #     is_exception = True
    #     error = "save_comuni failed %s" % e
    #     print(error)
    # if is_exception:
    #     raise TaskFailure(error)
    cursor = connection.cursor()
    sql_delete = (
        "delete from forecast_comuni where data_emissione='"
        + str(bulletin.data_emissione)
        + "'"
    )
    cursor.execute(sql_delete)
    print("elimino " + cursor.statusmessage + " record con " + sql_delete)

    print("inizio bulk_create su forecast_comuni")
    models.ForecastComuni.objects.bulk_create(forecast_comuni_array)
    fine = datetime.datetime.now()
    print(
        "bulk_create su forecast_comuni finito in ",
        abs((fine - inizio).total_seconds()),
        "secondi",
    )
    return "ok"


@celery_app.task(name="refresh_forecast_comuni", soft_time_limit=1200, time_limit=1200)
def refresh_forecast_comuni():
    time.sleep(
        5
    )  # aspetto 5 secondi per essere sicuro che il record del w35 sia stato salvato
    print("========== inizio refresh_forecast_comuni " + str(datetime.datetime.now()))
    delimiter = "__"
    result = ""
    inizio = datetime.datetime.now()
    cursor = connection.cursor()
    connection.connection.notices = deque()
    cursor.execute("select refresh_forecast_comuni()")
    for notice in connection.connection.notices:
        print(notice)
        result = result + notice
    fine = datetime.datetime.now()
    message = (
        "select refresh_forecast_comuni() finita in "
        + str(abs((fine - inizio).total_seconds()))
        + " secondi"
    )
    print(message)
    result = result + message
    message = (
        "tento il salvataggio delle temperature validate del bollettino meteo su forecast_comuni "
        + str(datetime.datetime.now())
    )
    print(message)
    result = result + message
    if (
        models_w05.W05.objects.filter(
            start_valid_time__year=inizio.year,
            start_valid_time__month=inizio.month,
            start_valid_time__day=inizio.day,
        )
        .filter(status="1")
        .exists()
    ):
        w05 = (
            models_w05.W05.objects.filter(
                start_valid_time__year=inizio.year,
                start_valid_time__month=inizio.month,
                start_valid_time__day=inizio.day,
            )
            .filter(status="1")
            .latest("last_update")
        )
        w05_datas = (
            models_w05.W05Data.objects.filter(
                id_venue__in=[1, 9, 11, 28, 33, 59, 63, 64]
            )
            .filter(id_w05=w05.id_w05)
            .filter(id_parametro="TERMA")
        )

        if (
            models.ForecastComuni.objects.filter(
                data_emissione__year=inizio.year,
                data_emissione__month=inizio.month,
                data_emissione__day=inizio.day,
            )
            .filter(id_comune__in=[860, 744, 1051, 576, 459, 272, 1196, 398])
            .exists()
        ):
            message = (
                "w35 send: salvo le temperature dei capoluoghi dal bollettino meteo"
            )
            print(message)
            result = result + message
            fcs_dict = {}
            fcs = models.ForecastComuni.objects.filter(
                data_emissione__year=inizio.year,
                data_emissione__month=inizio.month,
                data_emissione__day=inizio.day,
            ).filter(id_comune__in=[860, 744, 1051, 576, 459, 272, 1196, 398])
            for fc in fcs:
                fcs_dict[
                    str(fc.id_comune.id_comune)
                    + delimiter
                    + str(fc.id_time_layouts.id_time_layouts)
                ] = fc
            # print(fcs_dict)
            id_comune_to_id_venue = {
                9: 860,
                11: 744,
                1: 1051,
                28: 567,
                33: 459,
                59: 272,
                63: 1196,
                64: 398,
            }
            time_layouts_temperature_to_time_layouts = {
                50: 48,  # tmax pomD0
                68: 64,  # tmin matD1
                67: 65,  # tmax pomD1
                85: 81,  # tmin matD2
                84: 82,  # tmax pomD2
                102: 98,  # tmin matD3
                101: 99,  # tmax pomD3
            }
            for w05_data in w05_datas:
                # print("w05_data " + str(w05_data.id_venue.id_venue) + " " + w05_data.id_parametro.id_parametro +
                # " " + str(w05_data.id_aggregazione.id_aggregazione) + " " +
                # str(w05_data.id_time_layouts.id_time_layouts))
                id_comune = id_comune_to_id_venue[w05_data.id_venue.id_venue]
                if (
                    w05_data.id_time_layouts.id_time_layouts
                    in time_layouts_temperature_to_time_layouts
                ):
                    tl_fc = time_layouts_temperature_to_time_layouts[
                        w05_data.id_time_layouts.id_time_layouts
                    ]
                    # print("cerco in forecast_comuni " + str(id_comune) + delimiter + str(tl_fc))
                    if str(id_comune) + delimiter + str(tl_fc) in fcs_dict:
                        fc = fcs_dict[str(id_comune) + delimiter + str(tl_fc)]
                        # print("trovo " + fc)
                        if w05_data.id_parametro.id_parametro == "TERMA":
                            fc.air_temperature = w05_data.numeric_value
                            fc.trend = w05_data.id_trend.id_trend  # type: ignore
                            # print("fc", fc.id_time_layouts)

            fcs_list = []
            for fc in fcs_dict:  # type: ignore
                fcs_list.append(fcs_dict[fc])  # type: ignore
            models.ForecastComuni.objects.bulk_update(
                fcs_list, ["air_temperature", "trend"]
            )

    return result


class TaskFailure(Exception):
    pass
