# Generated by Django 2.0.4 on 2018-11-09 02:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0018_auto_20181102_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='period_late_begin',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 0, 14, 19, 613026)),
        ),
        migrations.AddField(
            model_name='place',
            name='period_late_end',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 0, 14, 19, 613026)),
        ),
        migrations.AddField(
            model_name='place',
            name='period_soon_begin',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 0, 14, 19, 613026)),
        ),
        migrations.AddField(
            model_name='place',
            name='period_soon_end',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 9, 0, 14, 19, 613026)),
        ),
    ]