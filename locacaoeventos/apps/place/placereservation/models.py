from django.db import models

from locacaoeventos.apps.place.placecore.models import Place
from django.contrib.auth.models import User

class PlacePrice(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    value = models.FloatField()
    value_min = models.FloatField()
    name = models.CharField(max_length=32)
    description_long = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    capacity_min = models.IntegerField()
    capacity_max = models.IntegerField()
    def __str__(self):
        return self.place.name + " - " + str(self.value_min)


class PlaceUnavailability(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    period = models.CharField(max_length=4) # min or max
    day = models.DateField()
    repeat = models.CharField(max_length=16, blank=True, null=True) # min or max

    def __str__(self):
        return self.place.name + " - " + str(self.day)


class PlaceReservation(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    placeprice = models.ForeignKey(PlacePrice, on_delete=models.CASCADE)
    buyer = models.ForeignKey("buyerprofile.BuyerProfile", on_delete=models.CASCADE)
    unavailability= models.OneToOneField(PlaceUnavailability, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now_add=True)
    pagarme_transaction = models.CharField(max_length=64, blank=True, null=True)
    def __str__(self):
        return self.place.name




class PlaceSazonality(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    day = models.DateField()
    modifier = models.IntegerField(blank=True, null=True) # min or max
    period = models.CharField(max_length=4, null=True) # min or max

    def __str__(self):
        return self.place.name + " - " + str(self.modifier)+'%'