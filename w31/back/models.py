from django.db import models

from website.core.models import Parametro, TimeLayouts

# TABELLE PRINCIPALI


class W31(models.Model):
    id_w31 = models.AutoField(primary_key=True)
    start_valid_time = models.DateTimeField()
    validity = models.IntegerField()
    next_blt_time = models.DateTimeField()
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    seq_num = models.BigIntegerField(blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    algoritmo = models.CharField(max_length=6)
    id_w31_parent = models.IntegerField(blank=True, null=True)
    annotazione = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w31"


# TABELLE REFERENCE


class W31Microaree(models.Model):
    id_w31_microaree = models.IntegerField(primary_key=True)
    nome_microarea_forestale = models.CharField(max_length=100)
    ettari_forestali = models.FloatField()

    class Meta:
        managed = False
        db_table = "w31_microaree"


class W31Macroaree(models.Model):
    id_w31_macroaree = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    ordine_bollettino = models.IntegerField()

    class Meta:
        managed = False
        db_table = "w31_macroaree"


class W31MicroMacroAree(models.Model):
    id_w31_micro_macro_aree = models.AutoField(primary_key=True)
    id_w31_microaree = models.ForeignKey(
        W31Microaree, models.DO_NOTHING, db_column="id_w31_microaree"
    )
    id_w31_macroaree = models.ForeignKey(
        W31Macroaree, models.DO_NOTHING, db_column="id_w31_macroaree"
    )

    class Meta:
        managed = False
        db_table = "w31_micro_macro_aree"


class W31Giorni(models.Model):
    id_w31_giorni = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "w31_giorni"


class W31Livelli(models.Model):
    id_w31_livelli = models.IntegerField(primary_key=True)
    colore = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "w31_livelli"


class W31AreeGiorniLivelli(models.Model):
    id_w31_aree_giorni_livelli = models.AutoField(primary_key=True)
    id_w31_microaree = models.ForeignKey(
        W31Microaree, models.DO_NOTHING, db_column="id_w31_microaree"
    )
    id_w31_giorni = models.ForeignKey(
        W31Giorni, models.DO_NOTHING, db_column="id_w31_giorni"
    )
    id_w31_livelli = models.ForeignKey(
        W31Livelli, models.DO_NOTHING, db_column="id_w31_livelli"
    )
    soglia_superiore = models.FloatField()

    class Meta:
        managed = False
        db_table = "w31_aree_giorni_livelli"


# TABELLE DATA


class W31DataMicroareeLivelli(models.Model):
    id_w31_data_microaree_livelli = models.AutoField(primary_key=True)
    id_w31 = models.ForeignKey(W31, on_delete=models.CASCADE, db_column="id_w31")
    id_w31_microaree = models.ForeignKey(
        W31Microaree, models.DO_NOTHING, db_column="id_w31_microaree"
    )
    id_w31_livelli = models.ForeignKey(
        W31Livelli, models.DO_NOTHING, db_column="id_w31_livelli"
    )
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )

    class Meta:
        managed = False
        db_table = "w31_data_microaree_livelli"


class W31DataMicroareeParametri(models.Model):
    id_w31_data_microaree_parametri = models.AutoField(primary_key=True)
    id_w31_data_microaree_livelli = models.ForeignKey(
        W31DataMicroareeLivelli,
        on_delete=models.CASCADE,
        db_column="id_w31_data_microaree_livelli",
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    numeric_value = models.FloatField()

    class Meta:
        managed = False
        db_table = "w31_data_microaree_parametri"


class W31DataMacroareeLivelli(models.Model):
    id_w31_data_macroaree_livelli = models.AutoField(primary_key=True)
    id_w31 = models.ForeignKey(W31, on_delete=models.CASCADE, db_column="id_w31")
    id_w31_macroaree = models.ForeignKey(
        W31Macroaree, models.DO_NOTHING, db_column="id_w31_macroaree"
    )
    id_w31_livelli = models.ForeignKey(
        W31Livelli, models.DO_NOTHING, db_column="id_w31_livelli"
    )
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )

    class Meta:
        managed = False
        db_table = "w31_data_macroaree_livelli"


class W31DataMacroareeParametri(models.Model):
    id_w31_data_macroaree_parametri = models.AutoField(primary_key=True)
    id_w31_data_macroaree_livelli = models.ForeignKey(
        W31DataMacroareeLivelli,
        on_delete=models.CASCADE,
        db_column="id_w31_data_macroaree_livelli",
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    numeric_value = models.FloatField()

    class Meta:
        managed = False
        db_table = "w31_data_macroaree_parametri"


# TABELLE ROLLING


class W31Rolling(models.Model):
    id_w31_microaree = models.ForeignKey(
        W31Microaree, models.DO_NOTHING, db_column="id_w31_microaree"
    )
    id_time_layouts = models.IntegerField()
    temp = models.FloatField()
    umid = models.FloatField()
    velv = models.FloatField()
    prec = models.FloatField()

    class Meta:
        managed = False
        db_table = "w31_rolling"


class W31Input(models.Model):
    id_w31_input = models.AutoField(primary_key=True)
    temp = models.FloatField()
    umid = models.FloatField()
    velv = models.FloatField()
    prec = models.FloatField()
    data = models.DateTimeField()
    id_w31_microaree = models.ForeignKey(
        W31Microaree, models.DO_NOTHING, db_column="id_w31_microaree"
    )

    class Meta:
        managed = False
        db_table = "w31_input"


class W31MacroareeInput(models.Model):
    id_w31_macroaree_input = models.AutoField(primary_key=True)
    id_w31_macroaree = models.ForeignKey(
        W31Macroaree, models.DO_NOTHING, db_column="id_w31_macroaree"
    )
    data = models.DateField()
    deltat = models.IntegerField()
    rh = models.IntegerField()
    ws = models.IntegerField()
    prec = models.IntegerField()

    class Meta:
        managed = False
        db_table = "w31_macroaree_input"
