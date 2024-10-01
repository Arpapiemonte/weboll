# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import Aggregazione, Parametro, TimeLayouts, Venue


class W36(models.Model):
    id_w36 = models.BigAutoField(primary_key=True)
    seq_num = models.IntegerField(blank=True, null=True)
    data_emissione = models.DateField()
    status = models.CharField(max_length=1)
    note = models.CharField(max_length=250)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    id_w36_parent = models.BigIntegerField(blank=True, null=True)
    chart_max = models.BinaryField(blank=True, null=True)
    chart_min = models.BinaryField(blank=True, null=True)
    internal_note = models.CharField(max_length=250)
    osservati = models.CharField(max_length=2000)
    debug = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = "w36"


class W36Data(models.Model):
    id_w36_data = models.BigAutoField(primary_key=True)
    id_w36 = models.ForeignKey(W36, models.DO_NOTHING, db_column="id_w36")
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    numeric_value = models.FloatField(blank=True, null=True)
    locked = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = "w36_data"
        unique_together = (
            "id_w36",
            "id_venue",
            "id_time_layouts",
            "id_parametro",
            "id_aggregazione",
        )


class W36Percentili(models.Model):
    id_w36_percentili = models.BigAutoField(primary_key=True)
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    mese = models.IntegerField()
    giorno = models.IntegerField()
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    numeric_value = models.FloatField(blank=True, null=True)
    numeric_value_bck = models.FloatField(blank=True, null=True)

    # def _get_mmgg(self):
    #    return '%s_%s' % (self.mese, self.giorno)
    # mmgg = property(_get_mmgg)

    class Meta:
        managed = False
        db_table = "w36_percentili"
        unique_together = (
            ("id_venue", "mese", "giorno", "id_parametro", "id_aggregazione"),
        )


class W36DecessiAttesi(models.Model):
    id_w36_decessi_attesi = models.BigAutoField(primary_key=True)
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    numeric_value = models.FloatField(blank=True, null=True)
    mese = models.IntegerField()
    giorno = models.IntegerField()

    class Meta:
        managed = False
        db_table = "w36_decessi_attesi"
        unique_together = (("id_venue", "mese", "giorno"),)


class W36ParametriEquazione(models.Model):
    id_w36_parametri = models.BigAutoField(primary_key=True)
    parametro_epid = models.CharField(unique=True, max_length=15)
    stima = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w36_parametri_equazione"


class MeteoRealTime(models.Model):
    id_rete_monit = models.CharField(max_length=2)
    codice_istat_comune = models.CharField(max_length=6, primary_key=True)
    progr_punto_com = models.IntegerField()
    data = models.DateField()
    ora = models.TimeField()
    id_parametro = models.CharField(max_length=8)
    id_aggregazione = models.IntegerField()
    valore_originale = models.DecimalField(
        max_digits=12, decimal_places=3, blank=True, null=True
    )
    valore_validato = models.DecimalField(
        max_digits=12, decimal_places=3, blank=True, null=True
    )
    tipologia_validaz = models.CharField(max_length=3, blank=True, null=True)
    flag_validaz_autom = models.CharField(max_length=1, blank=True, null=True)
    flag_gestore_sistema = models.CharField(max_length=1, blank=True, null=True)
    data_agg = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "meteo_real_time"
        unique_together = (
            (
                "codice_istat_comune",
                "progr_punto_com",
                "id_parametro",
            ),
        )
