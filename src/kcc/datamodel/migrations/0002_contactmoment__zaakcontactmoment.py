# Generated by Django 2.2 on 2019-10-23 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("datamodel", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="contactmoment",
            name="_zaakcontactmoment",
            field=models.URLField(
                blank=True,
                help_text="Link to the related object in the ZRC API",
                verbose_name="zaakcontactmoment",
            ),
        )
    ]
