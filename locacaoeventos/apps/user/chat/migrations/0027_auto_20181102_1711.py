# Generated by Django 2.0.4 on 2018-11-02 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0026_auto_20181102_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]