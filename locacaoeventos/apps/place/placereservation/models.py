from django.db import models

from locacaoeventos.apps.place.placecore.models import Place
from django.contrib.auth.models import User

class PlacePrice(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    value = models.FloatField("Valor")
    number_people = models.IntegerField("Número de pessoas", default=0)
    def __str__(self):
        return self.place.name


class PlaceUnavailability(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    datetime_begin = models.DateTimeField()
    datetime_end = models.DateTimeField()
    def __str__(self):
        return self.place.name


class PlaceReservation(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    placeprice = models.ForeignKey(PlacePrice, on_delete=models.CASCADE)
    buyer = models.ForeignKey("buyerprofile.BuyerProfile", on_delete=models.CASCADE)
    unavailability= models.OneToOneField(PlaceUnavailability, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.place.name
