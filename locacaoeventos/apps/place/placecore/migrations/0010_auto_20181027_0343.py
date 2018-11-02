# Generated by Django 2.0.4 on 2018-10-27 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0009_placefeature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placefeature',
            name='reservation_factor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='placefeature',
            name='reservation_factor_firstday',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='placefeature',
            name='review_factor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='placefeature',
            name='review_factor_firstday',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='placefeature',
            name='str_algorithm',
            field=models.CharField(blank=True, max_length=1028, null=True),
        ),
        migrations.AlterField(
            model_name='placefeature',
            name='view_factor',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='placefeature',
            name='view_factor_firstday',
            field=models.FloatField(blank=True, null=True),
        ),
    ]