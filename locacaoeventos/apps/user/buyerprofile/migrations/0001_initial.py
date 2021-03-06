# Generated by Django 2.0.4 on 2019-10-16 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Nome')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('cellphone', models.CharField(blank=True, max_length=64, null=True, verbose_name='Celular')),
                ('gender', models.CharField(blank=True, max_length=64, null=True, verbose_name='Sexo')),
                ('civil_status', models.CharField(blank=True, max_length=64, null=True, verbose_name='Status Civil')),
                ('cpf', models.CharField(blank=True, max_length=32, null=True, verbose_name='CPF')),
                ('is_active', models.BooleanField(default=True)),
                ('key', models.CharField(blank=True, max_length=64, null=True, verbose_name='Secret Key')),
                ('email', models.CharField(max_length=64, verbose_name='E-mail')),
                ('photo', models.FileField(blank=True, null=True, upload_to='buyerprofile/photo', verbose_name='Foto')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('accepts_newsletter', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Usuário Comprador+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Nome')),
                ('gender', models.CharField(max_length=64, verbose_name='Sexo')),
                ('birthday', models.DateField()),
                ('relation', models.CharField(max_length=64, verbose_name='Relation')),
                ('related_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Parentesco com+', to='buyerprofile.BuyerProfile')),
            ],
        ),
    ]
