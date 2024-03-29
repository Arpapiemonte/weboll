# Generated by Django 4.1.9 on 2023-07-21 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0011_auto_20220715_1655"),
    ]

    operations = [
        migrations.CreateModel(
            name="W33",
            fields=[
                ("id_w33", models.AutoField(primary_key=True, serialize=False)),
                ("id_w33_parent", models.IntegerField(blank=True, null=True)),
                ("data_emissione", models.DateField()),
                ("seq_num", models.IntegerField()),
                ("status", models.CharField(max_length=1)),
                ("last_update", models.DateTimeField()),
                ("username", models.CharField(max_length=30)),
            ],
            options={
                "db_table": "w33",
            },
        ),
        migrations.CreateModel(
            name="W33Data",
            fields=[
                ("id_w33_data", models.AutoField(primary_key=True, serialize=False)),
                ("cumulated_snow", models.IntegerField(null=True)),
                ("snow_level", models.IntegerField(null=True)),
                (
                    "id_sky_condition",
                    models.ForeignKey(
                        db_column="id_sky_condition",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.skycondition",
                    ),
                ),
                (
                    "id_time_layouts",
                    models.ForeignKey(
                        db_column="id_time_layouts",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.timelayouts",
                    ),
                ),
                (
                    "id_venue",
                    models.ForeignKey(
                        db_column="id_venue",
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="core.venue",
                    ),
                ),
                (
                    "id_w33",
                    models.ForeignKey(
                        db_column="id_w33",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="w33_back.w33",
                    ),
                ),
            ],
            options={
                "db_table": "w33_data",
            },
        ),
    ]
