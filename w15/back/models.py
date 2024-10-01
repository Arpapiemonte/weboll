# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import Aggregazione, Parametro, TimeLayouts, Venue


class W15(models.Model):
    id_w15 = models.BigAutoField(primary_key=True)
    seq_num = models.BigIntegerField(blank=True, null=True)
    data_emissione = models.DateTimeField()
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    id_w15_parent = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w15"


class W15Data(models.Model):
    id_w15_data = models.BigAutoField(primary_key=True)
    id_w15 = models.ForeignKey(W15, on_delete=models.CASCADE, db_column="id_w15")
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
    numeric_value = models.IntegerField(blank=True, null=True)
    id_trend = models.IntegerField(blank=True, null=False)

    class Meta:
        managed = False
        db_table = "w15_data"