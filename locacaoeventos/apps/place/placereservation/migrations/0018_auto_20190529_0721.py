# Generated by Django 2.0.4 on 2019-05-29 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placereservation', '0017_auto_20190529_0716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='placeprice',
            old_name='description_long',
            new_name='description',
        ),
    ]
