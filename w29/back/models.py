# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class W29(models.Model):
    id_w29 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    ora_emissione = models.CharField(max_length=5)
    ora_simulazione = models.CharField(max_length=5)
    numero_bollettino = models.CharField(max_length=30)
    situazione_evoluzione = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    data_validita = models.DateField()
    ora_osservazione = models.CharField(max_length=5, blank=True, null=True)
    data_osservazione = models.CharField(max_length=20, blank=True, null=True)
    data_simulazione = models.CharField(max_length=20, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    id_w29_parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w29"


class W29Data(models.Model):
    # id_w29 = models.OneToOneField(W29, models.DO_NOTHING, db_column='id_w29', primary_key=True)
    # Modificando in questo modo ho la visualizzazione completa della struttura dati prima era parziale
    # id_w29 = models.ForeignKey(W29, models.DO_NOTHING, db_column="id_w29", primary_key=True)
    id_w29_data = models.BigAutoField(primary_key=True)
    id_w29_zone = models.ForeignKey(
        "W29Zone", models.DO_NOTHING, db_column="id_w29_zone"
    )
    livello_criticita_oss = models.CharField(max_length=2)
    probabilita_criticita_oss = models.CharField(max_length=12)
    livello_criticita_prev_oggi = models.CharField(max_length=2)
    probabilita_criticita_prev_oggi = models.CharField(max_length=12)
    livello_criticita_prev_domani = models.CharField(max_length=2)
    probabilita_criticita_prev_domani = models.CharField(max_length=12)
    id_w29 = models.ForeignKey(W29, models.DO_NOTHING, db_column="id_w29")

    class Meta:
        managed = False
        db_table = "w29_data"


class W29Pericolo(models.Model):
    id_w29_pericolo = models.CharField(primary_key=True, max_length=2)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w29_pericolo"


class W29Probabilita(models.Model):
    id_w29_probabilita = models.CharField(primary_key=True, max_length=12)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w29_probabilita"


class W29Zone(models.Model):
    id_w29_zone = models.IntegerField(primary_key=True)
    descrizione = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w29_zone"
