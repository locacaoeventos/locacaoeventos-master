# Generated by Django 2.0.4 on 2018-11-02 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0017_delete_placeprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placevisualization',
            name='creation',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]