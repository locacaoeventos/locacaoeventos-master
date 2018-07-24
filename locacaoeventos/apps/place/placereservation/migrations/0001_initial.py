# Generated by Django 2.0.4 on 2018-07-24 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('buyerprofile', '0001_initial'),
        ('placecore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlacePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(verbose_name='Valor')),
                ('number_people', models.IntegerField(verbose_name='Número de pessoas')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placecore.Place')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyerprofile.BuyerProfile')),
                ('placeprice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placereservation.PlacePrice')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceUnavailability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_begin', models.DateTimeField()),
                ('datetime_end', models.DateTimeField()),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placecore.Place')),
            ],
        ),
        migrations.AddField(
            model_name='placereservation',
            name='unavailability',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='placereservation.PlaceUnavailability'),
        ),
    ]
