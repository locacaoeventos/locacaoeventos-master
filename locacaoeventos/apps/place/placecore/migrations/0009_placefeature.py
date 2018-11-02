# Generated by Django 2.0.4 on 2018-10-27 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0008_auto_20181027_0311'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_algorithm', models.CharField(max_length=1028)),
                ('view_factor', models.FloatField()),
                ('view_factor_firstday', models.FloatField()),
                ('reservation_factor', models.FloatField()),
                ('reservation_factor_firstday', models.FloatField()),
                ('review_factor', models.FloatField()),
                ('review_factor_firstday', models.FloatField()),
            ],
        ),
    ]