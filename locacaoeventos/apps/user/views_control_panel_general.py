from django.views.generic import View
from django.shortcuts import render, redirect

from locacaoeventos.apps.place.placecore.models import Place, PlaceLove, PlacePhoto

from locacaoeventos.utils.main import *


class UserLoved(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)

        context["extend_page"] = "control_panel/" + context["user_type"] + "_base.html"
        placeloves = PlaceLove.objects.filter(user=request.user)
        place_list = []

        for placelove in placeloves:
            place = placelove.place
            place_dic = placelove.place.__dict__
            place_dic["pk"] = place.pk
            place_dic["photo"] = PlacePhoto.objects.filter(place=place)[0].photo.photo
            place_list.append(place_dic)
        context["panel_type"] = "loved"
        context["place_list"] = place_list

        return render(request, "control_panel/buffet_loved.html", context)
