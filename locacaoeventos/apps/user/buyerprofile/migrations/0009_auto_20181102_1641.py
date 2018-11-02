# Generated by Django 2.0.4 on 2018-11-02 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('placecore', '0015_placeprice'),
        ('buyerprofile', '0008_auto_20181101_0323'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='placeprice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='placecore.PlacePrice'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='buyerprofile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyerprofile.BuyerProfile'),
        ),
    ]
