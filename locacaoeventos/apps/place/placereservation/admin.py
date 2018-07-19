from django.contrib import admin
from .models import PlacePrice, PlaceUnavailability, PlaceReservation

admin.site.register(PlacePrice)
admin.site.register(PlaceUnavailability)
admin.site.register(PlaceReservation)

