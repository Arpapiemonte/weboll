# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import Aggregazione, Parametro, TimeLayouts


class AreeAllertamento(models.Model):
    id_allertamento = models.CharField(primary_key=True, max_length=6)
    id_area = models.IntegerField()
    descrizione = models.CharField(max_length=50, blank=True, null=True)
    codice_istat_reg = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = "aree_allertamento"


class ForecastZone(models.Model):
    id_forecast_zone = models.AutoField(primary_key=True)
    id_allertamento = models.ForeignKey(
        AreeAllertamento,
        models.DO_NOTHING,
        db_column="id_allertamento",
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    model_name = models.CharField(max_length=9)
    model_type = models.CharField(max_length=5)
    data_emissione = models.DateTimeField()
    data_riferimento = models.DateTimeField()
    valore_originale = models.DecimalField(
        max_digits=12, decimal_places=3, blank=True, null=True
    )
    valore_validato = models.DecimalField(
        max_digits=12, decimal_places=3, blank=True, null=True
    )
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "forecast_zone"


class W30(models.Model):
    id_w30 = models.AutoField(primary_key=True)
    seq_num = models.BigIntegerField(blank=True, null=True)
    data_emissione = models.DateTimeField()
    data_prossimo_aggiornamento = models.DateTimeField()
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    id_w30_parent = models.IntegerField(blank=True, null=True)
    firstguess = models.TextField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = "w30"


class W30Data(models.Model):
    id_w30_data = models.AutoField(primary_key=True)
    id_w30 = models.ForeignKey(W30, on_delete=models.CASCADE, db_column="id_w30")
    id_allertamento = models.ForeignKey(
        AreeAllertamento, models.DO_NOTHING, db_column="id_allertamento"
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
    numeric_value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w30_data"
