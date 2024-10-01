# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import (
    Aggregazione,
    Parametro,
    Provincia,
    SkyCondition,
    StazioneMisura,
    TimeLayouts,
)


class AreeMeteo(models.Model):
    id_area_meteo = models.CharField(primary_key=True, max_length=6)
    id_area = models.IntegerField()
    descrizione = models.CharField(max_length=60, blank=True, null=True)
    top_y = models.IntegerField()
    left_x = models.IntegerField()

    class Meta:
        managed = False
        db_table = "aree_meteo"
        ordering = ["id_area"]


class RegioneOfficial(models.Model):
    codice_istat_reg = models.CharField(primary_key=True, max_length=2)
    denominazione = models.CharField(max_length=40)
    superficie = models.IntegerField(blank=True, null=True)
    data_agg = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "regione_official"


class ComuneOfficial(models.Model):
    id_comune = models.AutoField(primary_key=True)
    codice_regione = models.ForeignKey(
        RegioneOfficial, models.DO_NOTHING, db_column="codice_regione"
    )
    codice_provincia = models.ForeignKey(
        Provincia, models.DO_NOTHING, db_column="codice_provincia"
    )
    codice_comune = models.CharField(unique=True, max_length=6)
    codice_comune_old = models.CharField(max_length=6, blank=True, null=True)
    denominazione = models.CharField(max_length=40)
    latitudine_n = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True
    )
    longitudine_e = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True
    )
    x_wgs84 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    y_wgs84 = models.DecimalField(max_digits=7, decimal_places=0, blank=True, null=True)
    quota_comune = models.IntegerField()
    rank = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "comune_official"


class RelAreeMeteoComune(models.Model):
    id_area_meteo = models.OneToOneField(
        AreeMeteo, models.DO_NOTHING, db_column="id_area_meteo", primary_key=True
    )
    id_comune = models.ForeignKey(
        ComuneOfficial, models.DO_NOTHING, db_column="id_comune"
    )

    class Meta:
        managed = False
        db_table = "rel_aree_meteo_comune"
        unique_together = (("id_area_meteo", "id_comune"),)


class StazioniRappresentativeComune(models.Model):
    id_comune = models.OneToOneField(
        ComuneOfficial, models.DO_NOTHING, db_column="id_comune", primary_key=True
    )
    cod_staz_meteo_terma = models.ForeignKey(
        StazioneMisura,
        models.DO_NOTHING,
        db_column="cod_staz_meteo_terma",
        to_field="cod_staz_meteo",
        related_name="cod_staz_meteo_terma",
    )
    cod_staz_meteo_igro = models.ForeignKey(
        StazioneMisura,
        models.DO_NOTHING,
        db_column="cod_staz_meteo_igro",
        to_field="cod_staz_meteo",
        related_name="cod_staz_meteo_igro",
    )
    cod_staz_meteo_velv = models.ForeignKey(
        StazioneMisura,
        models.DO_NOTHING,
        db_column="cod_staz_meteo_velv",
        to_field="cod_staz_meteo",
        related_name="cod_staz_meteo_velv",
    )

    class Meta:
        managed = False
        db_table = "stazioni_rappresentative_comune"


class WeatherQuery(models.Model):
    id_query = models.BigAutoField(primary_key=True)
    parametro = models.CharField(max_length=10, blank=True, null=True)
    sql_text = models.TextField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "weather_query"


class WindClass(models.Model):
    code = models.SmallIntegerField(primary_key=True)
    description = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "wind_class"


class ForecastComuni(models.Model):
    id_comune = models.ForeignKey(
        ComuneOfficial, models.DO_NOTHING, db_column="id_comune"
    )
    data_emissione = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    sky_condition = models.ForeignKey(
        SkyCondition,
        models.DO_NOTHING,
        db_column="sky_condition",
        blank=True,
        null=True,
    )
    air_temperature = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    humidity = models.IntegerField(blank=True, null=True)
    wind_class = models.ForeignKey(
        WindClass, models.DO_NOTHING, db_column="wind_class", blank=True, null=True
    )
    wind_direction = models.CharField(max_length=5, blank=True, null=True)
    trend = models.SmallIntegerField(blank=True, null=True)
    snow_level = models.DecimalField(
        max_digits=7, decimal_places=0, blank=True, null=True
    )
    freezing_level = models.DecimalField(
        max_digits=7, decimal_places=0, blank=True, null=True
    )
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    id_forecast_comuni = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "forecast_comuni"
        unique_together = (("data_emissione", "id_time_layouts", "id_comune"),)


class W35(models.Model):
    id_w35 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    id_w35_parent = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w35"


class W35Data(models.Model):
    id_w35_data = models.BigAutoField(primary_key=True)
    id_w35 = models.ForeignKey(W35, models.DO_NOTHING, db_column="id_w35")
    id_area_meteo = models.ForeignKey(
        AreeMeteo, models.DO_NOTHING, db_column="id_area_meteo"
    )
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    numeric_value = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    ignore_refresh_forecast_comuni = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "w35_data"
        ordering = ["id_w35_data"]


class ForecastModels(models.Model):
    fore_name = models.CharField(primary_key=True, max_length=9)
    fore_type = models.CharField(max_length=5)
    fore_desc = models.CharField(max_length=60, blank=True, null=True)
    model_ris = models.CharField(max_length=4, blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "forecast_models"
        unique_together = (("fore_name", "fore_type"),)


class ForecastRuns(models.Model):
    id_forecast_run = models.BigAutoField(primary_key=True)
    # model_name = models.CharField(max_length=10)
    model_name = models.ForeignKey(
        ForecastModels, models.DO_NOTHING, db_column="model_name"
    )
    model_type = models.CharField(max_length=5)
    date_emiss = models.DateField()
    time_emiss = models.TimeField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "forecast_runs"


class ForecastStations(models.Model):
    id_forecast_station = models.BigAutoField(primary_key=True)
    id_forecast_run = models.ForeignKey(
        ForecastRuns, models.DO_NOTHING, db_column="id_forecast_run"
    )
    cod_staz_meteo = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = "forecast_stations"


class ForecastParameters(models.Model):
    id_forecast_parameter = models.BigAutoField(primary_key=True)
    id_forecast_station = models.ForeignKey(
        ForecastStations, models.DO_NOTHING, db_column="id_forecast_station"
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )

    class Meta:
        managed = False
        db_table = "forecast_parameters"


class ForecastValues(models.Model):
    id_forecast_value = models.BigAutoField(primary_key=True)
    id_forecast_parameter = models.ForeignKey(
        ForecastParameters, models.DO_NOTHING, db_column="id_forecast_parameter"
    )
    date_rif = models.DateField()
    time_rif = models.TimeField()
    value = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "forecast_values"
        unique_together = (("id_forecast_parameter", "date_rif", "time_rif"),)


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    worker = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()
    periodic_task_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "django_celery_results_taskresult"
