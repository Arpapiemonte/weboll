# Generated by Django 3.2.5 on 2021-07-20 15:19

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_auto_20210720_1416"),
    ]

    operations = [
        migrations.CreateModel(
            name="Destinazioni",
            fields=[
                (
                    "id_destinazione",
                    models.AutoField(primary_key=True, serialize=False),
                ),
                ("prodotto", models.TextField()),
                ("destinazione", models.TextField()),
                ("endpoint", models.TextField()),
                ("segreto", django_cryptography.fields.encrypt(models.TextField())),
            ],
            options={
                "db_table": "destinazioni",
                "managed": True,
            },
        ),
    ]