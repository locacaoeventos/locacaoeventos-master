# Generated by Django 2.0.4 on 2019-08-13 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placereservation', '0003_placesazonality_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placesazonality',
            name='modifier',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]