# Generated by Django 3.2.6 on 2021-08-14 07:37

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_destinazioni"),
    ]

    operations = [
        migrations.AddField(
            model_name="destinazioni",
            name="enabled",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="destinazioni",
            name="segreto",
            field=django_cryptography.fields.encrypt(models.TextField(blank=True)),
        ),
        migrations.AddField(
            model_name="destinazioni",
            name="auto",
            field=models.BooleanField(default=False),
        ),
    ]
