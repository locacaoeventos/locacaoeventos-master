# Generated by Django 2.0.4 on 2018-11-11 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placereservation', '0009_placeprice_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placeprice',
            name='number_people',
        ),
        migrations.AddField(
            model_name='placeprice',
            name='description',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='placeprice',
            name='name',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='placeprice',
            name='value',
            field=models.FloatField(),
        ),
    ]