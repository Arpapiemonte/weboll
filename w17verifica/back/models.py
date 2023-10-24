from django.db import models

from website.core.models import W05, Parametro


class w17_verifica(models.Model):
    id_w17verifica = models.BigAutoField(primary_key=True)
    data_analysis = models.DateField()
    data_emissione = models.DateField()
    next_blt_time = models.DateField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w17_verifica"


class w17_verifica_data(models.Model):
    id_w17verifica = models.ForeignKey(
        w17_verifica, models.DO_NOTHING, db_column="id_w17verifica"
    )
    id_w05 = models.ForeignKey(W05, models.DO_NOTHING, db_column="id_w05")
    # id_w05 = models.SmallIntegerField(blank=True, null=True)
    id_w17_verifica_data = models.BigAutoField(primary_key=True)
    data_forecast = models.DateField()
    forecast_id = models.SmallIntegerField(blank=True, null=True)
    punteggio_relativo = models.SmallIntegerField(blank=True, null=True)
    punteggio_nubi = models.SmallIntegerField(blank=True, null=True)
    punteggio_pioggia = models.SmallIntegerField(blank=True, null=True)
    punteggio_vento = models.SmallIntegerField(blank=True, null=True)
    punteggio_temperatura = models.SmallIntegerField(blank=True, null=True)
    punteggio_zero_quota_neve = models.SmallIntegerField(blank=True, null=True)
    coerenza_mattino_nubi = models.SmallIntegerField(blank=True, null=True)
    coerenza_pomeriggio_nubi = models.SmallIntegerField(blank=True, null=True)
    coerenza_mattino_pioggia = models.SmallIntegerField(blank=True, null=True)
    coerenza_pomeriggio_pioggia = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w17_verifica_data"


class w17_verifica_massimali(models.Model):
    id_w17_verifica_massimali = models.BigAutoField(primary_key=True)
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.SmallIntegerField(blank=True, null=True)
    categoria = models.SmallIntegerField(blank=True, null=True)
    punti_max = models.SmallIntegerField(blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w17_verifica_massimali"
