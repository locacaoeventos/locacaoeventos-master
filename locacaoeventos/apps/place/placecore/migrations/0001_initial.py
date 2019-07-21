# Generated by Django 2.0.4 on 2019-07-20 23:57

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellerprofile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoProvisory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(max_length=10485760, upload_to='place/photoprovisory', verbose_name='Foto')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('relevance', models.FloatField(default=0, verbose_name='Relevância')),
                ('feature', models.FloatField(default=0, verbose_name='Visualizações')),
                ('is_authorized_by_admin', models.BooleanField(default=False)),
                ('has_finished_basic', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('has_finished_payment', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=64, verbose_name='Nome')),
                ('address', models.CharField(max_length=256, verbose_name='Endereço')),
                ('description', models.CharField(max_length=1024, verbose_name='Descrição')),
                ('capacity', models.IntegerField(verbose_name='Capacidade')),
                ('video', models.CharField(blank=True, max_length=128, verbose_name='Video URL')),
                ('children_rides', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('decoration', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, size=None)),
                ('menu', models.FileField(blank=True, upload_to='place/menu', verbose_name='Menu')),
                ('period_soon_begin', models.TimeField(blank=True, null=True)),
                ('period_soon_end', models.TimeField(blank=True, null=True)),
                ('period_late_begin', models.TimeField(blank=True, null=True)),
                ('period_late_end', models.TimeField(blank=True, null=True)),
                ('lat', models.FloatField(verbose_name='Latitude')),
                ('lng', models.FloatField(verbose_name='Longitude')),
                ('sellerprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SellerProfile', to='sellerprofile.SellerProfile')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceAdditionalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_externalarea', models.BooleanField(verbose_name='Área externa')),
                ('has_childrenrides', models.BooleanField(verbose_name='Brinquedo pra Crianças')),
                ('has_thematicdecoration', models.BooleanField(verbose_name='Decoração Temática')),
                ('has_entertainment', models.BooleanField(verbose_name='Enterteinimento')),
                ('has_parking', models.BooleanField(verbose_name='Estacionamento')),
                ('has_costumes', models.BooleanField(verbose_name='Fantasias para os Atores')),
                ('has_babychangingroom', models.BooleanField(verbose_name='Fraldário')),
                ('has_illumination', models.BooleanField(verbose_name='Iluminação')),
                ('has_music', models.BooleanField(verbose_name='Música')),
                ('alcoholic_drink', models.BooleanField(verbose_name='Serve bebidas alcólicas')),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='placecore.Place')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('str_algorithm', models.CharField(blank=True, max_length=1028, null=True)),
                ('visualization_factor', models.FloatField(default=0)),
                ('visualization_factor_firstday', models.FloatField(default=0)),
                ('review_factor', models.FloatField(default=0)),
                ('review_factor_firstday', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceLove',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placecore.Place')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlacePhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_first', models.BooleanField(default=False)),
                ('photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='placecore.PhotoProvisory')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placecore.Place')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceVisualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='placecore.Place')),
            ],
        ),
    ]
