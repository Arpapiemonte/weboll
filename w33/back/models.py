# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import SkyCondition, TimeLayouts, Venue


class W33(models.Model):
    id_w33 = models.AutoField(primary_key=True)
    id_w33_parent = models.IntegerField(blank=True, null=True)
    data_emissione = models.DateField()
    seq_num = models.IntegerField()
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        db_table = "w33"


class W33Data(models.Model):
    id_w33_data = models.AutoField(primary_key=True)
    id_w33 = models.ForeignKey(W33, on_delete=models.CASCADE, db_column="id_w33")
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    id_sky_condition = models.ForeignKey(
        SkyCondition, models.DO_NOTHING, db_column="id_sky_condition"
    )
    cumulated_snow = models.IntegerField(null=True)
    snow_level = models.IntegerField(null=True)

    class Meta:
        db_table = "w33_data"
