# Generated by Django 2.0.4 on 2018-11-15 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('placereservation', '0013_placeunavailability_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeunavailability',
            name='day',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='placeunavailability',
            name='period',
            field=models.CharField(max_length=4),
        ),
    ]