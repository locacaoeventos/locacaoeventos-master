# Generated by Django 2.0.4 on 2018-07-23 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0005_place_has_finished_basic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='has_unavailability',
        ),
    ]
