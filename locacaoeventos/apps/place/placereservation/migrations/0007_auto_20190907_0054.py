# Generated by Django 2.0.4 on 2019-09-07 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placereservation', '0006_placereservation_cancelled'),
    ]

    operations = [
        migrations.RenameField(
            model_name='placereservation',
            old_name='cancelled',
            new_name='canceled',
        ),
    ]
