# Generated by Django 2.0.4 on 2018-08-26 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyerprofile', '0004_familymember_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='familymember',
            name='relation',
            field=models.CharField(max_length=64, verbose_name='Relation'),
        ),
    ]