# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BisBollettinoWebolimpia(models.Model):
    data = models.DateTimeField(blank=True, null=True)
    codice = models.CharField(primary_key=True, max_length=9, blank=True)
    # codice = models.CharField(max_length=9, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    h_min = models.FloatField(blank=True, null=True)
    h_max = models.FloatField(blank=True, null=True)
    h_med = models.FloatField(blank=True, null=True)
    q_min = models.FloatField(blank=True, null=True)
    q_max = models.FloatField(blank=True, null=True)
    q_med = models.FloatField(blank=True, null=True)
    corso_acqua = models.CharField(max_length=50, blank=True, null=True)
    localita = models.CharField(max_length=50, blank=True, null=True)
    id_note = models.IntegerField(blank=True, null=False)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "bis_bollettino_webolimpia"


class W26(models.Model):
    id_w26 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    numero_bollettino = models.CharField(max_length=30)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    data_validita = models.DateField()
    id_w26_parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w26"


class W26Zone(models.Model):
    id_w26_zone = models.BigAutoField(primary_key=True)
    codice = models.CharField(max_length=9, blank=True)
    localita = models.CharField(max_length=100)
    corsoacqua = models.CharField(max_length=100)
    numero = models.IntegerField()

    class Meta:
        managed = False
        db_table = "w26_zone"


class W26Data(models.Model):
    id_w26 = models.ForeignKey(W26, models.DO_NOTHING, db_column="id_w26")
    id_w26_zone = models.ForeignKey(
        "W26Zone", models.DO_NOTHING, db_column="id_w26_zone"
    )
    # localita = models.CharField(max_length=100)
    # corsoacqua = models.CharField(max_length=100)
    hmin = models.CharField(max_length=8, blank=True, null=True)
    hmax = models.CharField(max_length=8, blank=True, null=True)
    hmed = models.CharField(max_length=8, blank=True, null=True)
    qmin = models.CharField(max_length=8, blank=True, null=True)
    qmax = models.CharField(max_length=8, blank=True, null=True)
    qmed = models.CharField(max_length=8, blank=True, null=True)
    nota = models.CharField(max_length=2000, blank=True, null=True)
    idnota = models.CharField(max_length=70, blank=True, null=True)
    # numero = models.IntegerField()
    id_w26_data = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w26_data"
