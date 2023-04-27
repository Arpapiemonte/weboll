# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Regione(models.Model):
    codice_istat_reg = models.CharField(primary_key=True, max_length=1)
    denominazione = models.CharField(max_length=40)
    superficie = models.IntegerField(blank=True, null=True)
    data_agg = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "regione"


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


class StazioneMisura(models.Model):
    codice_istat_comune = models.OneToOneField(
        Comune, models.DO_NOTHING, db_column="codice_istat_comune", primary_key=True
    )
    progr_punto_com = models.IntegerField()
    codice_stazione = models.CharField(max_length=6, blank=True, null=True)
    nazione = models.CharField(max_length=30, blank=True, null=True)
    indirizzo_localita = models.CharField(max_length=80, blank=True, null=True)
    denominazione = models.CharField(unique=True, max_length=80)
    latitudine_n = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True
    )
    longitudine_e = models.DecimalField(
        max_digits=10, decimal_places=8, blank=True, null=True
    )
    latitudine_mm = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    longitudine_mm = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    utm_x = models.IntegerField(blank=True, null=True)
    utm_y = models.IntegerField(blank=True, null=True)
    quota_stazione = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    quota_sito = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    cod_staz_meteo = models.CharField(unique=True, max_length=5, blank=True, null=True)
    proprietario = models.CharField(max_length=100, blank=True, null=True)
    idtab_allertamento_2 = models.CharField(max_length=6, blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "stazione_misura"
        unique_together = (("codice_istat_comune", "progr_punto_com"),)


class W22Tendenza(models.Model):
    id_w22_tendenza = models.CharField(primary_key=True, max_length=2)
    descrizione = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w22_tendenza"


class W22Criticita(models.Model):
    id_w22_criticita = models.CharField(primary_key=True, max_length=2)
    descrizione = models.TextField(blank=True, null=True)
    colore_html = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w22_criticita"


class UnitaMisura(models.Model):
    id_unita_misura = models.CharField(primary_key=True, max_length=2)
    descrizione = models.CharField(max_length=60, blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "unita_misura"


class Aggregazione(models.Model):
    id_aggregazione = models.IntegerField(primary_key=True)
    descrizione = models.CharField(max_length=100)
    id_unita_misura = models.ForeignKey(
        "UnitaMisura",
        models.DO_NOTHING,
        db_column="id_unita_misura",
        blank=True,
        null=True,
    )
    tipo_aggregazione = models.CharField(max_length=1, blank=True, null=True)
    data_agg = models.DateTimeField(blank=True, null=True)
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "aggregazione"


class Parametro(models.Model):
    id_parametro = models.CharField(primary_key=True, max_length=15)
    denominazione = models.CharField(max_length=200)
    id_unita_misura = models.ForeignKey(
        "UnitaMisura",
        models.DO_NOTHING,
        db_column="id_unita_misura",
        blank=True,
        null=True,
    )
    num_decimali = models.IntegerField(blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "parametro"


class ReteMonitoraggio(models.Model):
    id_rete_monit = models.CharField(primary_key=True, max_length=2)
    denominazione = models.CharField(unique=True, max_length=100)
    data_validita = models.DateField()
    data_agg = models.DateField()
    autore_agg = models.CharField(max_length=30)
    sigla_rete = models.CharField(max_length=10, blank=True, null=True)
    ente_gestore = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "rete_monitoraggio"


class Previsioni_idrologiche_nwp(models.Model):
    id_modello = models.CharField(max_length=2, blank=True, null=True)
    id_nwp_model = models.CharField(max_length=6, blank=True, null=True)
    nwp_tof = models.DateField(blank=True, null=True)
    codice = models.CharField(primary_key=True, max_length=9)
    id_parametro = models.CharField(max_length=8, blank=True, null=True)
    tof = models.DateField(blank=True, null=True)
    dataora = models.DateField(blank=True, null=True)
    valore = models.FloatField()
    last_update = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "previsioni_idrologiche_nwp"


class MassimiStoriciIdrologici(models.Model):
    codice_istat_comune = models.CharField(primary_key=True, max_length=6)
    progr_punto_com = models.FloatField()
    data = models.DateField()
    id_parametro = models.CharField(max_length=8)
    valore = models.FloatField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    data_agg = models.DateField(blank=True, null=True)
    autore_agg = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "massimi_storici_idrologici"
        # unique_together = (
        #     ("codice_istat_comune", "progr_punto_com", "data", "id_parametro"),
        # )


class MeteoRealTimeIdro(models.Model):
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
        db_table = "meteo_real_time_idro"
        unique_together = (
            (
                "codice_istat_comune",
                "progr_punto_com",
                "id_parametro",
            ),
        )


class SoglieIdrometriche(models.Model):
    codice_istat_comune = models.CharField(primary_key=True, max_length=6)
    progr_punto_com = models.FloatField()
    id_parametro = models.CharField(max_length=8)
    codice1 = models.FloatField(blank=True, null=True)
    codice2 = models.FloatField(blank=True, null=True)
    codice3 = models.FloatField(blank=True, null=True)
    q_attenzione = models.FloatField(blank=True, null=True)
    dmv_base = models.FloatField(blank=True, null=True)
    dmv_deroga = models.FloatField(blank=True, null=True)
    data_agg = models.DateField(blank=True, null=True)
    autore_agg = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "soglie_idrometriche"
        unique_together = (("codice_istat_comune", "progr_punto_com", "id_parametro"),)


class W22(models.Model):
    id_w22 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    ora_emissione = models.CharField(max_length=5)
    data_validita = models.DateField()
    numero_bollettino = models.CharField(max_length=30)
    annotazione = models.TextField(blank=True, null=True)
    situazione_evoluzione = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    pdf_ordinario = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    validita = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w22"


class W22Zone(models.Model):
    id_w22_zone = models.IntegerField(primary_key=True)
    # id_w22_zone = models.AutoField(primary_key=True)
    # codice_istat_comune = models.ForeignKey(
    #     StazioneMisura, models.DO_NOTHING, db_column="codice_istat_comune"
    # )
    codice_istat_comune = models.CharField(max_length=80)
    progr_punto_com = models.IntegerField()
    denominazione_stazione = models.CharField(max_length=80)
    corso_acqua = models.CharField(max_length=30)
    id_parametro = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w22_zone"
        unique_together = (("codice_istat_comune", "progr_punto_com"),)


class W22Data(models.Model):
    id_w22 = models.ForeignKey(W22, models.DO_NOTHING, db_column="id_w22")
    id_w22_zone = models.ForeignKey(
        "W22Zone", models.DO_NOTHING, db_column="id_w22_zone"
    )
    codice1 = models.CharField(max_length=10, blank=True, null=True)
    codice2 = models.CharField(max_length=10, blank=True, null=True)
    codice3 = models.CharField(max_length=10, blank=True, null=True)
    tendenza6hprecedenti = models.CharField(max_length=15, blank=True, null=True)
    portata_attesa = models.CharField(max_length=15, blank=True, null=True)
    criticita_attesa = models.CharField(max_length=15, blank=True, null=True)
    prev_crit12h = models.CharField(max_length=15, blank=True, null=True)
    prev_crit24h = models.CharField(max_length=15, blank=True, null=True)
    prev_crit36h = models.CharField(max_length=15, blank=True, null=True)
    tend48h = models.CharField(max_length=15, blank=True, null=True)
    massimo_previsione = models.CharField(max_length=15, blank=True, null=True)
    data_massimo_storico = models.CharField(max_length=15, blank=True, null=True)
    valore_massimo_storico = models.CharField(max_length=15, blank=True, null=True)
    id_w22_data = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w22_data"
