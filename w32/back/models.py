# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class W32(models.Model):
    id_w32 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    ora_emissione = models.CharField(max_length=8)
    ora_simulazione = models.CharField(max_length=8)
    numero_bollettino = models.CharField(max_length=30)
    situazione_evoluzione = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    data_validita = models.DateField()
    ora_osservazione = models.CharField(max_length=8, blank=True, null=True)
    data_osservazione = models.CharField(max_length=20, blank=True, null=True)
    data_simulazione = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w32"


class W32Data(models.Model):
    id_w32 = models.ForeignKey(W32, models.DO_NOTHING, db_column="id_w32")
    id_w32_zone = models.ForeignKey(
        "W32Zone", models.DO_NOTHING, db_column="id_w32_zone"
    )
    livello_criticita_oss = models.CharField(max_length=2)
    livello_criticita_prev_oggi = models.CharField(max_length=2)
    livello_criticita_prev_domani = models.CharField(max_length=2)
    id_w32_data = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w32_data"


class W32MbaciniData(models.Model):
    id_w32 = models.ForeignKey(W32, models.DO_NOTHING, db_column="id_w32")
    id_w32_mbacini = models.ForeignKey(
        "W32Mbacini", models.DO_NOTHING, db_column="id_w32_mbacini"
    )
    livello_criticita_oss = models.CharField(max_length=2)
    livello_criticita_prev_oggi = models.CharField(max_length=2)
    livello_criticita_prev_domani = models.CharField(max_length=2)
    id_w32_mbacini_data = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w32_mbacini_data"


class W32Mbacini(models.Model):
    id_w32_mbacini = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=30)
    descrizione = models.CharField(max_length=100)
    ordinamento = models.IntegerField()

    class Meta:
        managed = False
        db_table = "w32_mbacini"


class W32Pericolo(models.Model):
    id_w32_pericolo = models.CharField(primary_key=True, max_length=2)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w32_pericolo"


class W32Pericolombacini(models.Model):
    id_w32_pericolombacini = models.CharField(primary_key=True, max_length=2)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w32_pericolombacini"


class W32Zone(models.Model):
    id_w32_zone = models.IntegerField(primary_key=True)
    descrizione = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w32_zone"
