# Generated by Django 2.0.4 on 2018-10-27 06:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20181027_0341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 27, 3, 43, 9, 638342), verbose_name='Datetime'),
        ),
    ]