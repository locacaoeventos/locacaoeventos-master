# Generated by Django 2.0.4 on 2018-07-24 01:48

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
            name='SellerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=64, verbose_name='Nome')),
                ('email', models.CharField(max_length=64, verbose_name='E-mail')),
                ('cpf', models.CharField(max_length=32, verbose_name='CPF')),
                ('cnpj', models.CharField(max_length=32, verbose_name='CNPJ')),
                ('is_active', models.BooleanField(default=True)),
                ('key', models.CharField(blank=True, max_length=64, null=True, verbose_name='Secret Key')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
