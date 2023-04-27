# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SoglieNivoAreaPrev(models.Model):
    idtab_allertamento = models.CharField(primary_key=True, max_length=6)
    ambito = models.CharField(max_length=10)
    soglia_cod1 = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True
    )
    soglia_cod2 = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True
    )
    soglia_cod3 = models.DecimalField(
        max_digits=5, decimal_places=1, blank=True, null=True
    )
    data_agg = models.DateField()
    autore_agg = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "soglie_nivo_area_prev"
        unique_together = (("idtab_allertamento", "ambito"),)


class SogliePluvAreaPrevMassimi(models.Model):
    idtab_allertamento = models.CharField(primary_key=True, max_length=6)
    codice_allertamento = models.CharField(max_length=1)
    h1 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h3 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h6 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h12 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h24 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    data_agg = models.DateField()
    autore_agg = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "soglie_pluv_area_prev_massimi"
        unique_together = (("idtab_allertamento", "codice_allertamento"),)


class SogliePluvAreaPrevMedie(models.Model):
    idtab_allertamento = models.CharField(primary_key=True, max_length=6)
    codice_allertamento = models.CharField(max_length=1)
    h6 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h12 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h24 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h48 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    h72 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    data_agg = models.DateField()
    autore_agg = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "soglie_pluv_area_prev_medie"
        unique_together = (("idtab_allertamento", "codice_allertamento"),)


class W23(models.Model):
    id_w23 = models.BigAutoField(primary_key=True)
    data_emissione = models.DateField()
    numero_bollettino = models.CharField(max_length=30)
    situazione_meteo = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    fraserisknat = models.TextField(blank=True, null=True)
    annotazione = models.TextField(blank=True, null=True)
    last_update_annotazione = models.DateTimeField()
    id_w23_parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w23"


# gli attributi "related_name" non sono stati messi da "inspectdb" e all'avvio di django dava errori
class W23Data(models.Model):
    id_w23 = models.ForeignKey(W23, models.DO_NOTHING, db_column="id_w23")
    id_w23_zone = models.ForeignKey(
        "W23Zone", models.DO_NOTHING, db_column="id_w23_zone"
    )
    idrogeologico_oggi = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idrogeologico_oggi",
        db_column="idrogeologico_oggi",
    )
    idrogeologico_domani = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idrogeologico_domani",
        db_column="idrogeologico_domani",
    )
    temporali_oggi = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="temporali_oggi",
        db_column="temporali_oggi",
    )
    temporali_domani = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="temporali_domani",
        db_column="temporali_domani",
    )
    idraulico_oggi = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idraulico_oggi",
        db_column="idraulico_oggi",
    )
    idraulico_domani = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idraulico_domani",
        db_column="idraulico_domani",
    )
    neve_oggi = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="neve_oggi",
        db_column="neve_oggi",
    )
    neve_domani = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="neve_domani",
        db_column="neve_domani",
    )
    valanghe_oggi = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="valanghe_oggi",
        db_column="valanghe_oggi",
    )
    valanghe_domani = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="valanghe_domani",
        db_column="valanghe_domani",
    )
    scenario_atteso = models.TextField(blank=True, null=True)
    idrogeologico_oggi_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idrogeologico_oggi_for",
        db_column="idrogeologico_oggi_for",
        blank=True,
        null=True,
    )
    idrogeologico_domani_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idrogeologico_domani_for",
        db_column="idrogeologico_domani_for",
        blank=True,
        null=True,
    )
    temporali_oggi_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="temporali_oggi_for",
        db_column="temporali_oggi_for",
        blank=True,
        null=True,
    )
    temporali_domani_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="temporali_domani_for",
        db_column="temporali_domani_for",
        blank=True,
        null=True,
    )
    idraulico_oggi_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idraulico_oggi_for",
        db_column="idraulico_oggi_for",
        blank=True,
        null=True,
    )
    idraulico_domani_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="idraulico_domani_for",
        db_column="idraulico_domani_for",
        blank=True,
        null=True,
    )
    neve_oggi_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="neve_oggi_for",
        db_column="neve_oggi_for",
        blank=True,
        null=True,
    )
    neve_domani_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="neve_domani_for",
        db_column="neve_domani_for",
        blank=True,
        null=True,
    )
    valanghe_oggi_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="valanghe_oggi_for",
        db_column="valanghe_oggi_for",
        blank=True,
        null=True,
    )
    valanghe_domani_for = models.ForeignKey(
        "W23Pericolo",
        models.DO_NOTHING,
        related_name="valanghe_domani_for",
        db_column="valanghe_domani_for",
        blank=True,
        null=True,
    )
    scenario_atteso_for = models.TextField(blank=True, null=True)
    pluvmax12hd0 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax12hd1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax24hd1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h18g0 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h00g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h06g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h12g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h18g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h00g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h06g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h12g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h18g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmax6h00g3 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h18g0 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h00g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h06g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h12g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h18g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h00g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h06g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h12g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h18g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed6h00g3 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h18g0_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h00g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h06g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h12g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h18g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h00g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h06g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h12g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h18g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed12h00g3 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h18g0_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h00g1_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h06g1_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h12g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h18g1 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h00g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h06g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h12g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h18g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed24h00g3 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h18g0_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h00g1_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h06g1_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h12g1_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h18g1_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h00g2_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h06g2_oss = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h12g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h18g2 = models.CharField(max_length=5, blank=True, null=True)
    pluvmed48h00g3 = models.CharField(max_length=5, blank=True, null=True)
    neveqmin = models.CharField(max_length=5, blank=True, null=True)
    neveqmax = models.CharField(max_length=5, blank=True, null=True)
    neve400_oggi = models.CharField(max_length=5, blank=True, null=True)
    neve400_domani = models.CharField(max_length=5, blank=True, null=True)
    neve400_totale = models.CharField(max_length=5, blank=True, null=True)
    neve700_oggi = models.CharField(max_length=5, blank=True, null=True)
    neve700_domani = models.CharField(max_length=5, blank=True, null=True)
    neve700_totale = models.CharField(max_length=5, blank=True, null=True)
    neve1000_oggi = models.CharField(max_length=5, blank=True, null=True)
    neve1000_domani = models.CharField(max_length=5, blank=True, null=True)
    neve1000_totale = models.CharField(max_length=5, blank=True, null=True)
    temporale_oggi = models.CharField(max_length=40, blank=True, null=True)
    temporale_domani = models.CharField(max_length=40, blank=True, null=True)
    neveqd01 = models.CharField(max_length=5, blank=True, null=True)
    neveqd02 = models.CharField(max_length=5, blank=True, null=True)
    neveqd11 = models.CharField(max_length=5, blank=True, null=True)
    neveqd12 = models.CharField(max_length=5, blank=True, null=True)
    neveqd13 = models.CharField(max_length=5, blank=True, null=True)
    neveqd14 = models.CharField(max_length=5, blank=True, null=True)
    id_w23_data = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w23_data"


class W23Effettiterritorio(models.Model):
    id_w23_effettiterritorio = models.CharField(primary_key=True, max_length=2)
    descrizione = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w23_effettiterritorio"


class W23Pericolo(models.Model):
    id_w23_pericolo = models.CharField(primary_key=True, max_length=10)
    colore_html = models.CharField(max_length=30)
    sort_index = models.IntegerField()

    class Meta:
        managed = False
        db_table = "w23_pericolo"


class W23Pluvossh6(models.Model):
    data = models.DateField()
    ora = models.TimeField()
    area = models.CharField(max_length=7)
    valore = models.CharField(max_length=20, blank=True, null=True)
    id_w23_pluvossh6 = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w23_pluvossh6"


class W23Zone(models.Model):
    id_w23_zone = models.IntegerField(primary_key=True)
    zona_allerta = models.CharField(max_length=2)
    bacino = models.CharField(max_length=40)
    provincia = models.CharField(max_length=20)
    nome_zona = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w23_zone"
