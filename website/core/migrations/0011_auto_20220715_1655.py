# Generated by Django 4.0.5 on 2022-07-15 16:55

from django.db import migrations


def populate_bulletins(apps, schema_editor):
    BulletinsModel = apps.get_model("core", "bulletins")
    BulletinsModel.objects.get_or_create(prodotto="psa", tabella="w30")
    BulletinsModel.objects.get_or_create(prodotto="vigilanza", tabella="w24")
    BulletinsModel.objects.get_or_create(prodotto="allerta", tabella="w23")
    BulletinsModel.objects.get_or_create(prodotto="incendi", tabella="w31")
    BulletinsModel.objects.get_or_create(prodotto="defense", tabella="w32")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_alter_bulletins_tabella"),
    ]

    operations = [
        migrations.RunPython(populate_bulletins),
    ]
