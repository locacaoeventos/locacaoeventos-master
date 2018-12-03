from django.db import models

from locacaoeventos.apps.place.placecore.models import Place
from django.contrib.auth.models import User

class PlacePrice(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    value = models.FloatField()
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    capacity_min = models.IntegerField()
    capacity_max = models.IntegerField()
    def __str__(self):
        return self.place.name + " - " + str(self.value)


class PlaceUnavailability(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    period = models.CharField(max_length=4) # min or max
    day = models.DateField()
    def __str__(self):
        return self.place.name + " - " + str(self.day)


class PlaceReservation(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    placeprice = models.ForeignKey(PlacePrice, on_delete=models.CASCADE)
    buyer = models.ForeignKey("buyerprofile.BuyerProfile", on_delete=models.CASCADE)
    unavailability= models.OneToOneField(PlaceUnavailability, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.place.name
