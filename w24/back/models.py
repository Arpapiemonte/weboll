# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Aggregazione(models.Model):
    id_aggregazione = models.IntegerField(primary_key=True)
    descrizione = models.CharField(max_length=100)
    id_unita_misura = models.ForeignKey(
        "UnitaMisura",
        models.DO_NOTHING,
        db_column="id_unita_misura",
        blank=True,
        null=True,
    )
    tipo_aggregazione = models.CharField(max_length=1, blank=True, null=True)
    data_agg = models.DateTimeField(blank=True, null=True)
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "aggregazione"


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
        "Parametro", models.DO_NOTHING, db_column="id_parametro"
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


class Parametro(models.Model):
    id_parametro = models.CharField(primary_key=True, max_length=10)
    denominazione = models.CharField(max_length=200)
    id_unita_misura = models.ForeignKey(
        "UnitaMisura",
        models.DO_NOTHING,
        db_column="id_unita_misura",
        blank=True,
        null=True,
    )
    num_decimali = models.IntegerField(blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "parametro"


class TimeLayouts(models.Model):
    id_time_layouts = models.IntegerField(primary_key=True)
    start_day_offset = models.SmallIntegerField()
    end_day_offset = models.SmallIntegerField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "time_layouts"


class UnitaMisura(models.Model):
    id_unita_misura = models.CharField(primary_key=True, max_length=2)
    descrizione = models.CharField(max_length=60, blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "unita_misura"


class W24(models.Model):
    id_w24 = models.BigAutoField(primary_key=True)
    numero_bollettino = models.CharField(max_length=30)
    data_emissione = models.DateField()
    next_blt_time = models.DateField()
    sintesi_meteo = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    tipo_anomalia_termica = models.CharField(max_length=1, blank=True, null=True)
    forzante_0 = models.CharField(max_length=1)
    forzante_1 = models.CharField(max_length=1)
    forzante_2 = models.CharField(max_length=1)
    id_w24_parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w24"


class W24Data(models.Model):
    id_w24 = models.ForeignKey(W24, models.DO_NOTHING, db_column="id_w24")
    id_allertamento = models.ForeignKey(
        AreeAllertamento, models.DO_NOTHING, db_column="id_allertamento"
    )
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    numeric_value = models.DecimalField(max_digits=7, decimal_places=2)
    id_w24_data = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w24_data"


class W24Soglie(models.Model):
    id_allertamento = models.CharField(primary_key=True, max_length=6)
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    soglia1 = models.DecimalField(max_digits=7, decimal_places=2)
    soglia2 = models.DecimalField(max_digits=7, decimal_places=2)
    classe_intensita = models.IntegerField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w24_soglie"
        unique_together = (
            ("id_allertamento", "id_parametro", "id_aggregazione", "classe_intensita"),
        )
