from django.shortcuts import render, redirect
from django.views.generic import View

from datetime import datetime
import ast

from locacaoeventos.utils.main import *
from .placecore.models import Place

class BuyPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        capacity = request.GET.get("capacidade")
        place_pk = request.GET.get("place_pk")
        date = ast.literal_eval(request.GET.get("date").replace(" ",""))

        place = Place.objects.get(pk=place_pk)
        date = datetime.strptime(date[0] + date[1] + date[2], "%d%m%Y")

        return render(request, "place_buy.html", context)

