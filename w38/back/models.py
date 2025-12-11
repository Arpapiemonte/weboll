# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import Aggregazione, Parametro, TimeLayouts


class W38DatiIvrea(models.Model):
    id_w38 = models.BigAutoField(primary_key=True)
    id_venue = models.IntegerField(blank=True, null=True)
    data_emissione = models.DateField()
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    numeric_value = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w38_dati_ivrea"


class W38(models.Model):
    id_w38 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    data_validita = models.DateField()
    numero_bollettino = models.CharField(max_length=30)
    situazione_evoluzione = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    note = models.TextField(blank=True, null=True)
    id_w38_parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w38"


class W38Data(models.Model):
    id_w38_data = models.AutoField(primary_key=True)
    id_w38 = models.ForeignKey(W38, on_delete=models.CASCADE, db_column="id_w38")
    id_venue = models.CharField(max_length=30)
    # id_venue = models.ForeignKey(
    #     Venue, models.DO_NOTHING, db_column="id_venue"
    # )
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

    class Meta:
        managed = False
        db_table = "w38_data"
