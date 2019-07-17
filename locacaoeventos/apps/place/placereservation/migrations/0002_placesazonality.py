# Generated by Django 2.0.4 on 2019-07-09 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0001_initial'),
        ('placereservation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceSazonality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('modifier', models.IntegerField(blank=True, max_length=5, null=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placecore.Place')),
            ],
        ),
    ]