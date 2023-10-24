from django.db import models

from website.core.models import (
    Aggregazione,
    Classes,
    ClassesValue,
    Parametro,
    TimeLayouts,
    Venue,
)


class W17(models.Model):
    id_w17 = models.BigAutoField(primary_key=True)
    data_analysis = models.DateField()
    data_emissione = models.DateField()
    next_blt_time = models.DateField()
    situation = models.TextField(blank=True, null=True)
    cloudiness = models.TextField(blank=True, null=True)
    weather_code = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)
    status = models.CharField(max_length=1, blank=True, null=True)
    numero_bollettino = models.CharField(max_length=30)
    id_w17_parent = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w17"


class W17Blob(models.Model):
    id_w17 = models.OneToOneField(
        W17, models.DO_NOTHING, db_column="id_w17", primary_key=True
    )
    situation_image = models.BinaryField(blank=True, null=True)
    cloudiness_image = models.BinaryField(blank=True, null=True)
    prec_mattino_image = models.BinaryField(blank=True, null=True)
    prec_pomeriggio_image = models.BinaryField(blank=True, null=True)
    temp_minime_image = models.BinaryField(blank=True, null=True)
    temp_massime_image = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w17_blob"


class W17Classes(models.Model):
    id_w17 = models.ForeignKey(W17, models.DO_NOTHING, db_column="id_w17")
    id_w17_classes = models.BigAutoField(primary_key=True)
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_classes_value = models.ForeignKey(
        ClassesValue, models.DO_NOTHING, db_column="id_classes_value"
    )
    id_classes = models.ForeignKey(Classes, models.DO_NOTHING, db_column="id_classes")
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )

    class Meta:
        managed = False
        db_table = "w17_classes"
        unique_together = (
            ("id_w17", "id_classes_value", "id_classes", "id_time_layouts"),
        )


class W17Data(models.Model):
    id_w17 = models.ForeignKey(W17, models.DO_NOTHING, db_column="id_w17")
    id_w17_data = models.BigAutoField(primary_key=True)
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    id_parametro = models.ForeignKey(
        Parametro, models.DO_NOTHING, db_column="id_parametro"
    )
    id_aggregazione = models.ForeignKey(
        Aggregazione, models.DO_NOTHING, db_column="id_aggregazione"
    )
    numeric_value = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    id_trend = models.SmallIntegerField(blank=True, null=True)
    text_value = models.TextField(blank=True, null=True)
    cod_staz_meteo = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w17_data"
        unique_together = (
            (
                "id_w17",
                "id_venue",
                "id_time_layouts",
                "id_parametro",
                "id_aggregazione",
            ),
        )
