# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import SkyCondition, TimeLayouts, Venue


class W07(models.Model):
    id_w07 = models.BigAutoField(primary_key=True)
    id_w07_parent = models.IntegerField(blank=True, null=True)
    start_valid_time = models.DateTimeField()
    validity = models.IntegerField()
    next_blt_time = models.DateTimeField()
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = "w07"


class W07Data(models.Model):
    id_w07 = models.ForeignKey(W07, models.DO_NOTHING, db_column="id_w07")
    id_w07_data = models.AutoField(primary_key=True)
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    sky_condition = models.ForeignKey(
        SkyCondition, models.DO_NOTHING, db_column="sky_condition"
    )
    precipitation_class = models.SmallIntegerField(blank=True, null=True)
    cumulated_snow = models.IntegerField(blank=True, null=True)
    freezing_level = models.IntegerField(blank=True, null=True)
    snow_level = models.IntegerField(blank=True, null=True)
    temperature_below_zero = models.BooleanField(blank=True, null=True)
    air_temperature = models.IntegerField(blank=True, null=True)
    wind_class = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "w07_data"
        unique_together = (("id_w07", "id_venue", "id_time_layouts"),)
