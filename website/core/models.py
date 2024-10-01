#
# Copyright (C) 2024 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt
#
#

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_cryptography.fields import encrypt


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


class Application(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    code = models.CharField(unique=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)
    userapplicationfqn = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "application"


class Applicationgroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "applicationgroup"


class Applicationrole(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    descritpion = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(unique=True, max_length=255)
    application = models.ForeignKey(Application, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "applicationrole"


class Apuser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    enabled = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = "apuser"


class Classes(models.Model):
    id_classes = models.SmallIntegerField(primary_key=True)
    id_parametro = models.ForeignKey(
        "Parametro", models.DO_NOTHING, db_column="id_parametro"
    )
    description = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    version = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "classes"


class ClassesValue(models.Model):
    id_classes_value = models.SmallIntegerField(primary_key=True)
    id_classes = models.ForeignKey(
        Classes,
        on_delete=models.DO_NOTHING,
        related_name="classes_value",
        db_column="id_classes",
    )
    description = models.CharField(max_length=50)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "classes_value"


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


class ForecastModels(models.Model):
    fore_name = models.CharField(primary_key=True, max_length=9)
    fore_type = models.CharField(max_length=5)
    fore_desc = models.CharField(max_length=60, blank=True, null=True)
    model_ris = models.CharField(max_length=4, blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "forecast_models"
        unique_together = (("fore_name", "fore_type"),)


class Groupapplicationrole(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    role = models.ForeignKey(Applicationrole, models.DO_NOTHING)
    group = models.ForeignKey(Applicationgroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "groupapplicationrole"


class OzonoAggregazione(models.Model):
    id_ozono_aggregazione = models.SmallIntegerField(primary_key=True)
    aggregazione = models.CharField(max_length=20)
    desc_aggregazione_spaziale = models.CharField(max_length=30)
    desc_aggregazione_temporale = models.CharField(max_length=60)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "ozono_aggregazione"


class OzonoLivelli(models.Model):
    id_ozono_livelli = models.SmallIntegerField(primary_key=True)
    livelli = models.IntegerField()
    soglia_inferiore_mxd = models.IntegerField()
    soglia_superiore_mxd = models.IntegerField()
    soglia_inferiore_mx8 = models.IntegerField()
    soglia_superiore_mx8 = models.IntegerField()
    riferimento_legge = models.TextField()
    colore = models.CharField(max_length=20)
    rgb = models.TextField()
    sintesi_raccomandazioni = models.TextField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    raccomandazione = models.TextField(blank=True, null=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "ozono_livelli"
        unique_together = (("livelli", "valid_from", "valid_to"),)


class OzonoZone(models.Model):
    id_ozono_zone = models.SmallIntegerField(primary_key=True)
    zone = models.CharField(max_length=1)
    descrizione = models.CharField(max_length=60)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "ozono_zone"
        unique_together = (("zone", "valid_from", "valid_to"),)


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


class Products(models.Model):
    id_products = models.CharField(primary_key=True, max_length=4)
    description = models.CharField(max_length=50)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "products"


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


class QaMisure(models.Model):
    id_qa_misure = models.AutoField(primary_key=True)
    id_venue = models.IntegerField()
    data_emissione = models.DateTimeField()
    data_scadenza = models.DateTimeField()
    id_scadenza = models.IntegerField(blank=True, null=True)
    id_strumentazione = models.SmallIntegerField()
    id_qa_aggregazione = models.SmallIntegerField()
    id_qa_parametro = models.CharField(max_length=10)
    valore_originale_num = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    valore_validato_num = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    valore_originale_classe = models.IntegerField(blank=True, null=True)
    valore_validato_classe = models.IntegerField(blank=True, null=True)
    valore_originale_txt = models.TextField(blank=True, null=True)
    valore_validato_txt = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "qa_misure"


class Regione(models.Model):
    codice_istat_reg = models.CharField(primary_key=True, max_length=1)
    denominazione = models.CharField(max_length=40)
    superficie = models.IntegerField(blank=True, null=True)
    data_agg = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "regione"


class RelWeatherProdParameter(models.Model):
    id_rel_weather_prod_parameter = models.IntegerField(primary_key=True)
    id_products = models.ForeignKey(
        Products, models.DO_NOTHING, db_column="id_products"
    )
    id_venue = models.ForeignKey("Venue", models.DO_NOTHING, db_column="id_venue")
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    cod_staz_meteo = models.CharField(max_length=5, blank=True, null=True)
    fore_name = models.CharField(max_length=9, blank=True, null=True)
    fore_type = models.CharField(max_length=5, blank=True, null=True)
    priority = models.IntegerField()
    validation_flag = models.BooleanField(blank=True, null=True)
    valid_to = models.DateTimeField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "rel_weather_prod_parameter"


class RelWeatherProdTimeLayouts(models.Model):
    id_rel_weather_prod_time_layouts = models.IntegerField(primary_key=True)
    id_rel_weather_prod_parameter = models.ForeignKey(
        RelWeatherProdParameter,
        models.DO_NOTHING,
        db_column="id_rel_weather_prod_parameter",
    )
    id_time_layouts = models.ForeignKey(
        "TimeLayouts", models.DO_NOTHING, db_column="id_time_layouts"
    )
    valid_to = models.DateTimeField(blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "rel_weather_prod_time_layouts"


class SkyCondition(models.Model):
    id_sky_condition = models.SmallIntegerField(primary_key=True)
    sky_condition = models.CharField(max_length=6)
    description = models.CharField(max_length=60)
    description_ita = models.CharField(max_length=60)
    image = models.BinaryField()
    alt_code = models.CharField(max_length=6)
    sort_index = models.SmallIntegerField(blank=True, null=True)
    id_infile = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "sky_condition"


class SkyConditionClasses(models.Model):
    id_classes_value = models.SmallIntegerField(primary_key=True)
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    ordinamento = models.IntegerField()
    id_sky_condition = models.ForeignKey(
        SkyCondition,
        models.DO_NOTHING,
        related_name="classes",
        db_column="id_sky_condition",
    )

    class Meta:
        managed = False
        db_table = "sky_condition_classes"


class SkyCover(models.Model):
    id_sky_cover = models.AutoField(primary_key=True)
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)
    desc_ita = models.CharField(max_length=120, blank=True, null=True)
    desc_eng = models.CharField(max_length=120, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sky_cover"


class StazioneMeteo(models.Model):
    codice_istat_comune = models.CharField(primary_key=True, max_length=6)
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
        db_table = "stazione_meteo"
        unique_together = (("codice_istat_comune", "progr_punto_com"),)


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


class Sensore(models.Model):
    codice_istat_comune = models.OneToOneField(
        StazioneMisura,
        models.DO_NOTHING,
        db_column="codice_istat_comune",
        primary_key=True,
    )
    progr_punto_com = models.IntegerField()
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    codice_sensore_das = models.IntegerField(blank=True, null=True)
    num_decimale_cae = models.IntegerField(blank=True, null=True)
    tempo_campionamento = models.IntegerField(blank=True, null=True)
    tempo_registrazione = models.IntegerField(blank=True, null=True)
    altezza_sensore = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    data_installazione = models.DateField(blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "sensore"
        unique_together = (("codice_istat_comune", "progr_punto_com", "id_parametro"),)


class SensoreStazioneMisura(models.Model):
    codice_istat_comune = models.CharField(max_length=6, primary_key=True)
    progr_punto_com = models.IntegerField(blank=True, null=True)
    cod_staz_meteo = models.CharField(max_length=5, blank=True, null=True)
    denominazione = models.CharField(max_length=80, blank=True, null=True)
    id_parametro = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = "sensore_stazione_misura"
        unique_together = (("codice_istat_comune", "progr_punto_com", "id_parametro"),)


class TimeLayouts(models.Model):
    id_time_layouts = models.IntegerField(primary_key=True)
    start_day_offset = models.SmallIntegerField()
    end_day_offset = models.SmallIntegerField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    day_offset = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "time_layouts"


class Trend(models.Model):
    id_trend = models.SmallIntegerField(primary_key=True)
    id_web = models.SmallIntegerField()
    desc_ita = models.CharField(max_length=50, blank=True, null=True)
    desc_eng = models.CharField(max_length=50, blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "trend"


class UnitaMisura(models.Model):
    id_unita_misura = models.CharField(primary_key=True, max_length=2)
    descrizione = models.CharField(max_length=60, blank=True, null=True)
    data_agg = models.DateTimeField()
    autore_agg = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "unita_misura"


class Userauth(models.Model):
    name = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "userauth"


class Usergroup(models.Model):
    id = models.BigIntegerField(primary_key=True)
    version = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey(Apuser, models.DO_NOTHING)
    group = models.ForeignKey(Applicationgroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "usergroup"
        unique_together = (("user", "group"),)


class Venue(models.Model):
    id_venue = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=50)
    altitude = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True
    )
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "venue"


class W05(models.Model):
    id_w05 = models.BigAutoField(primary_key=True)
    start_valid_time = models.DateTimeField()
    validity = models.IntegerField()
    next_blt_time = models.DateTimeField()
    situation = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    seq_num = models.BigIntegerField(blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    id_w05_parent = models.IntegerField(blank=True, null=True)
    situation_image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w05"


class W05Classes(models.Model):
    id_w05_classes = models.AutoField(primary_key=True)
    id_w05 = models.ForeignKey(W05, models.DO_NOTHING, db_column="id_w05")
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    id_classes_value = models.ForeignKey(
        ClassesValue, models.DO_NOTHING, db_column="id_classes_value"
    )
    id_classes = models.ForeignKey(Classes, models.DO_NOTHING, db_column="id_classes")
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    start_valid_time = models.DateTimeField()
    end_valid_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "w05_classes"
        ordering = ["id_classes"]


class W05Conf(models.Model):
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    descr = models.CharField(primary_key=True, max_length=50)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w05_conf"
        unique_together = (("descr", "id_venue"),)


class W05Data(models.Model):
    id_w05_data = models.AutoField(primary_key=True)
    id_w05 = models.ForeignKey(W05, models.DO_NOTHING, db_column="id_w05")
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    numeric_value = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    id_trend = models.ForeignKey(
        Trend, models.DO_NOTHING, db_column="id_trend", blank=True, null=True
    )
    text_value = models.TextField(blank=True, null=True)
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    start_valid_time = models.DateTimeField()
    end_valid_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "w05_data"


class W16(models.Model):
    id_w16 = models.AutoField(primary_key=True)
    start_valid_time = models.DateTimeField()
    validity = models.IntegerField()
    next_blt_time = models.DateTimeField()
    made_by = models.CharField(max_length=1)
    note = models.TextField()
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    seq_num = models.BigIntegerField(blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    id_w16_parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w16"


class W16Conf(models.Model):
    id_w16_conf = models.IntegerField(primary_key=True)
    id_ozono_aggregazione = models.ForeignKey(
        OzonoAggregazione, models.DO_NOTHING, db_column="id_ozono_aggregazione"
    )
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w16_conf"


class W16Data(models.Model):
    id_w16_data = models.AutoField(primary_key=True)
    id_w16 = models.ForeignKey(W16, models.DO_NOTHING, db_column="id_w16")
    id_ozono_zone = models.ForeignKey(
        OzonoZone, models.DO_NOTHING, db_column="id_ozono_zone"
    )
    data_emissione = models.DateTimeField()
    data_scadenza = models.DateTimeField()
    id_scadenza = models.IntegerField()
    id_ozono_livelli = models.ForeignKey(
        OzonoLivelli, models.DO_NOTHING, db_column="id_ozono_livelli"
    )

    class Meta:
        managed = False
        db_table = "w16_data"


class W16Data1(models.Model):
    id_w16_data = models.ForeignKey(W16Data, models.DO_NOTHING, db_column="id_w16_data")
    id_qa_parametro = models.CharField(max_length=10)
    id_ozono_aggregazione = models.ForeignKey(
        OzonoAggregazione, models.DO_NOTHING, db_column="id_ozono_aggregazione"
    )
    valore_num = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    valore_classe = models.IntegerField(blank=True, null=True)
    id_w16_data1 = models.AutoField(primary_key=True)
    id_strumentazione = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w16_data1"
        ordering = ["pk", "id_ozono_aggregazione"]


class WeatherAttribute(models.Model):
    id_weather_attribute = models.IntegerField(primary_key=True)
    desc_ita = models.CharField(max_length=240, blank=True, null=True)
    desc_eng = models.CharField(max_length=240, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "weather_attribute"


class WeatherValue(models.Model):
    id_weather_value = models.IntegerField(primary_key=True)
    desc_ita = models.CharField(max_length=160, blank=True, null=True)
    desc_eng = models.CharField(max_length=160, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "weather_value"


class WeatherValues(models.Model):
    id_weather_values = models.AutoField(primary_key=True)
    # id_venue = models.IntegerField()
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # id_time_layouts = models.IntegerField()
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    # id_parametro = models.CharField(max_length=10)
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    # id_aggregazione = models.IntegerField()
    original_numeric_values = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    validated_numeric_values = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    original_text_values = models.TextField(blank=True, null=True)
    validated_text_values = models.TextField(blank=True, null=True)
    original_trend = models.ForeignKey(
        Trend,
        models.DO_NOTHING,
        db_column="original_trend",
        related_name="original_trend",
        blank=True,
        null=True,
    )
    validated_trend = models.ForeignKey(
        Trend,
        models.DO_NOTHING,
        db_column="validated_trend",
        related_name="validated_trend",
        blank=True,
        null=True,
    )
    id_query_numeric = models.BigIntegerField(blank=True, null=True)
    id_query_text = models.BigIntegerField(blank=True, null=True)
    cod_staz_meteo = models.CharField(max_length=5, blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "weather_values"
        unique_together = (
            (
                "id_venue",
                "start_time",
                "end_time",
                "id_time_layouts",
                "id_parametro",
                "id_aggregazione",
            ),
        )


class Bulletins(models.Model):
    prodotto = models.TextField(primary_key=True)
    tabella = models.TextField(null=True)
    auto = models.BooleanField(default=False)
    time = models.TimeField(default="12:30")

    class Meta:
        managed = True
        db_table = "bollettini"
        verbose_name_plural = "Bulletins"


class Destinazioni(models.Model):
    id_destinazione = models.AutoField(primary_key=True)
    prodotto = models.ForeignKey(Bulletins, models.DO_NOTHING, db_column="prodotto")
    destinazione = models.TextField()
    endpoint = models.TextField()
    segreto = encrypt(models.TextField(blank=True))
    enabled = models.BooleanField(default=True)
    auto = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "destinazioni"
        verbose_name_plural = "Destinazioni"
