# Generated by Django 2.0.4 on 2018-08-03 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0002_auto_20180803_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(max_length=256, verbose_name='Endereço'),
        ),
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.CharField(max_length=128, verbose_name='Descrição'),
        ),
    ]