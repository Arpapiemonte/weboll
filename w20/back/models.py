# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TrapsComuni(models.Model):
    data = models.DateField(blank=True, null=True)
    comune = models.CharField(max_length=80, blank=True, null=True)
    frane_tot = models.SmallIntegerField(blank=True, null=True)
    frane_sup1 = models.SmallIntegerField(blank=True, null=True)
    frane_sup2 = models.SmallIntegerField(blank=True, null=True)
    stato = models.SmallIntegerField(blank=True, null=True)
    codice = models.IntegerField(blank=True, null=True)
    gid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "traps_comuni"
        unique_together = (("data", "comune"),)


class W20(models.Model):
    id_w20 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    numero_bollettino = models.CharField(max_length=30)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    pioggia_infiltrata = models.BinaryField(blank=True, null=True)
    neve_equivalente = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w20"


class W20Data(models.Model):
    id_w20 = models.ForeignKey(W20, models.DO_NOTHING, db_column="id_w20")
    id_w20_zone = models.IntegerField()
    id_w20_data = models.AutoField(primary_key=True)
    provincia = models.CharField(max_length=100)
    comune = models.CharField(max_length=100)
    if_perc = models.CharField(max_length=100)
    prob_innesco = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "w20_data"
        unique_together = (("id_w20", "provincia", "comune"),)


class W20Pericolo(models.Model):
    id_w20_pericolo = models.CharField(primary_key=True, max_length=2)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w20_pericolo"


class W20Zone(models.Model):
    id_w20_zone = models.IntegerField(primary_key=True)
    comune = models.CharField(max_length=30)
    provincia = models.CharField(max_length=20)
    if_perc = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "w20_zone"
