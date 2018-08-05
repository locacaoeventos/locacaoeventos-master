from django.db import models

from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile
from locacaoeventos.apps.place.placecore.models import Place
from django.contrib.auth.models import User

class PlacePrice(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    value = models.FloatField("Valor")
    number_people = models.IntegerField("Número de pessoas", default=0)



class PlaceUnavailability(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    datetime_begin = models.DateTimeField()
    datetime_end = models.DateTimeField()


class PlaceReservation(models.Model):
    placeprice = models.ForeignKey(PlacePrice, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    unavailability= models.OneToOneField(PlaceUnavailability, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
