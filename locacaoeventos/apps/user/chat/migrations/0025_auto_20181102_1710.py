# Generated by Django 2.0.4 on 2018-11-02 20:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0024_auto_20181102_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 2, 17, 10, 42, 448245), verbose_name='Datetime'),
        ),
    ]