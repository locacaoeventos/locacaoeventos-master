# Generated by Django 2.0.4 on 2018-09-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0004_auto_20180803_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='placephoto',
            name='is_first',
            field=models.BooleanField(default=False),
        ),
    ]