# Generated by Django 2.0.4 on 2018-11-02 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0015_placeprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placeprice',
            name='place',
        ),
    ]