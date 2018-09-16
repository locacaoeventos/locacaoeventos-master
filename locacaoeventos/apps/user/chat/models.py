from django.db import models

from django.contrib.auth.models import User
from locacaoeventos.apps.place.placecore.models import Place

import datetime

class Message(models.Model):
    text = models.CharField("Texto", max_length=1024)
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_from')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_to')
    datetime = models.DateTimeField("Datetime", default=datetime.datetime.now())
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
