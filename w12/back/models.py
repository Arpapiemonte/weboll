# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from website.core.models import SkyCondition, TimeLayouts, Venue


class W12(models.Model):
    id_w12 = models.AutoField(primary_key=True)
    id_w12_parent = models.IntegerField(blank=True, null=True)
    start_valid_time = models.DateTimeField()
    validity = models.IntegerField()
    next_blt_time = models.DateTimeField()
    status = models.CharField(max_length=1)
    last_update = models.DateTimeField()
    username = models.CharField(max_length=30)

    class Meta:
        db_table = "w12"


class W12Data(models.Model):
    id_w12_data = models.AutoField(primary_key=True)
    id_w12 = models.ForeignKey(W12, on_delete=models.CASCADE, db_column="id_w12")
    id_venue = models.ForeignKey(Venue, models.DO_NOTHING, db_column="id_venue")
    id_time_layouts = models.ForeignKey(
        TimeLayouts, models.DO_NOTHING, db_column="id_time_layouts"
    )
    sky_condition = models.ForeignKey(
        SkyCondition, models.DO_NOTHING, db_column="sky_condition"
    )
    cloud_amount = models.IntegerField(null=True)
    precipitation_class = models.IntegerField(null=True)
    cumulated_snow = models.IntegerField(null=True)
    freezing_level = models.IntegerField(null=True)
    snow_level = models.IntegerField(null=True)
    temperature_below_zero = models.BooleanField()
    risk_freezing_rain = models.BooleanField()
    vis_inf_1000 = models.BooleanField()
    vis_inf_1000_reason = models.IntegerField(null=True)
    wind_class = models.IntegerField(null=True)

    class Meta:
        db_table = "w12_data"
