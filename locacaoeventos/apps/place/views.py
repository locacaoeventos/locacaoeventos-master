from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import datetime, calendar

from locacaoeventos.utils.main import *
from locacaoeventos.utils.place import *
from locacaoeventos.utils.general import *
from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile

from .placecore.models import Place, PlacePhoto, PlaceAdditionalInformation
from .placereservation.models import PlacePrice, PlaceUnavailability, PlaceReservation
from .placereview.models import PlaceReview


class ListPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        place_list = []
        for place in Place.objects.filter(is_active=True):
            place_list.append({
                "pk": place.pk,
                "size": place.size,
                "name": place.name,
                "capacity": place.capacity,
                "address": place.address,
                "description": place.description,
                "photo": PlacePhoto.objects.filter(place=place)[0].photo.photo
            })


        # BEGIN Paginator
        paginator = Paginator(place_list, 6)
        page = request.GET.get('page')
        places = paginator.get_page(page)
        places.paginator.place_range = [item+1 for item in range(places.paginator.num_pages)]
        context["place_list"] = places
        # END Paginator


        # Left Panel
        context["place_additional_information"] = get_additional_information_important_attributes()
        context["capacity"] = request.GET.get("capacity")
        context["address"] = request.GET.get("place")
        print(get_latlng_with_address_str(context["address"]))
        context["date"] = request.GET.get("date")

        return render(request, "place_list.html", context)




class DetailPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context = detailplace_context(context, self.request)
        return render(request, "place_detail.html", context)


    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        context = detailplace_context(context, self.request)
        description = self.request.POST["description"]
        rate = self.request.POST["rate"]
        PlaceReview.objects.create(
            user=self.request.user,
            description=description,
            rate=rate,
            place=context["place_obj"]
        )
        return render(request, "place_detail.html", context)






def detailplace_context(context, request):
    place_obj = Place.objects.get(pk=request.GET["pk"])
    place = place_obj.__dict__
    context["place_seller"] = place_obj.sellerprofile.__dict__
    context["place"] = place
    context["place_pk"] = place_obj.pk
    context["place_obj"] = place_obj
    context["place_photo"] = PlacePhoto.objects.filter(place=place_obj)[0].photo.photo
    context["photo_list"] = [photo.photo for photo in PlacePhoto.objects.filter(place=place_obj)]

    context["additionalinformation"] = []

    additionalinformation = PlaceAdditionalInformation.objects.get(place=place_obj).__dict__
    additionalinformation_attributes = get_additional_information_important_attributes()
    for key in additionalinformation:
        if additionalinformation[key] == True and key != "id" and key != "place_id":
            context["additionalinformation"].append({
                "key_name": key,
                "name": get_dic_by_key(listdic=additionalinformation_attributes, key="name", value=key)["label"],
            })


    reviews_dic = get_reviews_from_place(place_obj)
    context["review_list"] = reviews_dic["review_list"]
    context["review_rates"] = reviews_dic["review_rates"]

    return context


def get_additional_information_important_attributes():
    return [
        {
            "name": "alcoholic_drink",
            "label": "Serve bebidas alcólicas"
        },
        {
            "name": "has_entertainment",
            "label": "Enterteinimento"
        },
        {
            "name": "has_thematicdecoration",
            "label": "Decoração Temática"
        },
        {
            "name": "has_childrenrides",
            "label": "Brinquedo pra Crianças"
        },
        {
            "name": "has_costumes",
            "label": "Fantasias para os Atores"
        },
        {
            "name": "has_parking",
            "label": "Estacionamento"
        },
        {
            "name": "has_externalarea",
            "label": "Área externa"
        },
        {
            "name": "has_music",
            "label": "Música"
        },
        {
            "name": "has_illumination",
            "label": "Iluminação"
        },
        {
            "name": "has_babychangingroom",
            "label": "Fraldário"
        },
    ]