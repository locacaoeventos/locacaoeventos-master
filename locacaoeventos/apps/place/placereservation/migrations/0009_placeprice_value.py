# Generated by Django 2.0.4 on 2018-11-11 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placereservation', '0008_auto_20181110_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeprice',
            name='value',
            field=models.FloatField(default=0, verbose_name='Valor'),
            preserve_default=False,
        ),
    ]
