# Generated by Django 2.0.4 on 2018-12-03 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyerprofile', '0014_auto_20181123_0028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='buyerprofile',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='place',
        ),
        migrations.RemoveField(
            model_name='shoppingcart',
            name='placeprice',
        ),
        migrations.DeleteModel(
            name='ShoppingCart',
        ),
    ]
