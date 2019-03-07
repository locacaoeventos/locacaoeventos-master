from django.db import models
from django.utils import timezone

from locacaoeventos.apps.place.placecore.models import Place
from locacaoeventos.apps.place.placereservation.models import PlaceReservation
from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile
from django.contrib.auth.models import User

class PlaceReview(models.Model):
    reservation = models.OneToOneField(PlaceReservation, on_delete=models.CASCADE)
    buyerprofile = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now=True)
    comment = models.CharField("Description", max_length=256, blank=True, null=True)
    rate_infraestructure = models.IntegerField()
    rate_rides = models.IntegerField()
    rate_cost_benefit = models.IntegerField()
    rate_attendance = models.IntegerField()
    rate_children_opinion = models.IntegerField()

    def get_average_rate(self):
        average_rate = (self.rate_infraestructure + self.rate_rides + self.rate_cost_benefit + self.rate_attendance + self.rate_children_opinion)/5
        return average_rate

    def __str__(self):
        return "Review de " + self.reservation.unavailability.place.name + " - " + str(self.creation)