# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core import models as models_w05


class Comune(models.Model):
    codice_istat_comune = models.CharField(primary_key=True, max_length=6)
    denominazione = models.CharField(max_length=40)
    codice_istat_81 = models.CharField(max_length=5, blank=True, null=True)
    codice_istat_92 = models.CharField(max_length=6)
    cap = models.IntegerField(blank=True, null=True)
    codice_istat_prov = models.ForeignKey(
        "Provincia",
        models.DO_NOTHING,
        db_column="codice_istat_prov",
        blank=True,
        null=True,
    )
    latitudine_n = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True
    )
    longitudine_e = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True
    )
    codice_meteo_it = models.IntegerField(blank=True, null=True)
    quota_comune = models.IntegerField(blank=True, null=True)
    data_agg = models.DateField()

    class Meta:
        managed = False
        db_table = "comune"


class Provincia(models.Model):
    codice_istat_prov = models.CharField(primary_key=True, max_length=3)
    sigla_auto = models.CharField(max_length=2)
    denominazione = models.CharField(max_length=40)
    codice_istat_1981 = models.CharField(max_length=2, blank=True, null=True)
    codice_istat_reg = models.ForeignKey(
        "Regione",
        models.DO_NOTHING,
        db_column="codice_istat_reg",
        blank=True,
        null=True,
    )
    data_agg = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "provincia"


class Regione(models.Model):
    codice_istat_reg = models.CharField(primary_key=True, max_length=1)
    denominazione = models.CharField(max_length=40)
    superficie = models.IntegerField(blank=True, null=True)
    data_agg = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "regione"


class W22Zone(models.Model):
    id_w22_zone = models.AutoField(primary_key=True)
    codice_istat_comune = models.ForeignKey(
        models_w05.StazioneMisura, models.DO_NOTHING, db_column="codice_istat_comune"
    )
    progr_punto_com = models.IntegerField()
    denominazione_stazione = models.CharField(max_length=80)
    corso_acqua = models.CharField(max_length=30)
    id_parametro = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w22_zone"
        unique_together = (("codice_istat_comune", "progr_punto_com"),)


class W22Giudizio(models.Model):
    id_w22giudizio = models.BigIntegerField(primary_key=True)
    descrizione = models.TextField(blank=True, null=True)
    colore_html = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w22giudizio"


class W22verificaCriticita(models.Model):
    id_w22_criticita = models.CharField(primary_key=True, max_length=2)
    descrizione = models.TextField(blank=True, null=True)
    colore_html = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w22verifica_criticita"


class W22Severita(models.Model):
    id_w22severita = models.BigIntegerField(primary_key=True)
    sigla = models.CharField(max_length=3)
    descrizione = models.TextField(blank=True, null=True)
    colore_html = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w22severita"


class W22Verifica(models.Model):
    id_w22verifica = models.BigAutoField(primary_key=True)
    # id_w22 = models.BigIntegerField()
    id_numero_bollettino = models.CharField(max_length=30)
    numero_bollettino = models.CharField(max_length=30)
    data_emissione = models.DateField()
    data_analisi = models.DateField()
    id_w22giudizio = models.BigIntegerField()
    # id_w22giudizio = models.ForeignKey(
    #    W22Giudizio, models.DO_NOTHING, db_column="id_w22giudizio"
    # )
    annotazione = models.TextField(blank=True, null=True)
    situazione_evoluzione = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w22verifica"


class W22VerificaData(models.Model):
    id_w22verifica = models.ForeignKey(
        W22Verifica, models.DO_NOTHING, db_column="id_w22verifica"
    )
    id_w22_zone = models.ForeignKey(W22Zone, models.DO_NOTHING, db_column="id_w22_zone")
    prev_crit_tot = models.CharField(max_length=15, blank=True, null=True)
    # prev_crit24h = models.CharField(max_length=15, blank=True, null=True)
    # prev_crit36h = models.CharField(max_length=15, blank=True, null=True)
    oss_crit_tot = models.CharField(max_length=15, blank=True, null=True)
    err_crit_tot = models.CharField(max_length=15, blank=True, null=True)
    # oss_crit24h = models.CharField(max_length=15, blank=True, null=True)
    # oss_crit36h = models.CharField(max_length=15, blank=True, null=True)
    id_w22verifica_data = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w22verifica_data"
