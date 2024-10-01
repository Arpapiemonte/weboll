# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class W37(models.Model):
    id_w37 = models.BigAutoField(primary_key=True)
    numero_bollettino = models.IntegerField(blank=True, null=True)
    data_emissione = models.DateTimeField()
    ora_emissione = models.CharField(max_length=5)
    data_aggiornamento = models.DateField()
    ora_aggiornamento = models.CharField(max_length=5)
    situazione_attuale = models.TextField(blank=True, null=True)
    previsione_meteo = models.TextField(blank=True, null=True)
    previsione_idro = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    id_w37_parent = models.IntegerField(blank=True, null=True)
    mappa_3h = models.BinaryField(blank=True, null=True)
    mappa_24h = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w37"


class W37Data(models.Model):
    id_w37_data = models.AutoField(primary_key=True)
    id_w37 = models.ForeignKey(W37, on_delete=models.CASCADE, db_column="id_w37")
    comune = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    sigla_prov = models.CharField(max_length=30)
    pericolo = models.IntegerField(blank=True, null=True)
    pluvio = models.IntegerField(blank=True, null=True)
    idro = models.IntegerField(blank=True, null=True)
    temporali = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w37_data"
