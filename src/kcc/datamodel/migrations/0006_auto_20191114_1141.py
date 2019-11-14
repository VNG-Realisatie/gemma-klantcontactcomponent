# Generated by Django 2.2.6 on 2019-11-14 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("datamodel", "0005_auto_20191114_1410"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactmoment",
            name="klant",
            field=models.ForeignKey(
                blank=True,
                help_text="URL-referentie naar een KLANT (in de Contactmomenten API)",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="datamodel.Klant",
            ),
        ),
        migrations.AlterField(
            model_name="klant",
            name="achternaam",
            field=models.CharField(
                blank=True, help_text="De achternaam van de klant.", max_length=200
            ),
        ),
        migrations.AlterField(
            model_name="klant",
            name="adres",
            field=models.CharField(
                blank=True, help_text="Het adres van de klant.", max_length=1000
            ),
        ),
        migrations.AlterField(
            model_name="klant",
            name="betrokkene",
            field=models.URLField(
                blank=True, help_text="URL-referentie naar een subject", max_length=1000
            ),
        ),
        migrations.AlterField(
            model_name="klant",
            name="betrokkene_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("natuurlijk_persoon", "Natuurlijk persoon"),
                    ("vestiging", "Vestiging"),
                ],
                help_text="Type van de `subject`.",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="klant",
            name="emailadres",
            field=models.EmailField(
                blank=True, help_text="Het e-mail adres van de klant.", max_length=254
            ),
        ),
        migrations.AlterField(
            model_name="klant",
            name="telefoonnummer",
            field=models.CharField(
                blank=True,
                help_text="Het mobiele of vaste telefoonnummer van de klant.",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="klant",
            name="voornaam",
            field=models.CharField(
                blank=True,
                help_text="De voornaam, voorletters of roepnaam van de klant.",
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="contactmoment",
            name="klant",
            field=models.ForeignKey(
                blank=True,
                help_text="URL-referentie naar een KLANT (in de Contactmomenten API) indien het contactmoment niet anoniem is.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="datamodel.Klant",
            ),
        ),
    ]
