# Generated by Django 2.0.4 on 2018-10-27 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_auto_20181027_0436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 27, 14, 3, 22, 662843), verbose_name='Datetime'),
        ),
    ]
