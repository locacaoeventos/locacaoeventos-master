from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.serializers.json import DjangoJSONEncoder

import datetime, calendar, json, ast

from locacaoeventos.utils.general import *
from locacaoeventos.utils.main import *
from locacaoeventos.utils.place import *
from locacaoeventos.utils.user import *
from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile

from .placecore.models import Place, PlacePhoto, PlaceAdditionalInformation, PlaceVisualization, PlaceLove
from .placereservation.models import PlacePrice, PlaceUnavailability, PlaceReservation, PlacePrice
from .placereview.models import PlaceReview


class ListPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        place_list_not_filtered = get_place_information(Place.objects.filter(is_active=True, has_finished_basic=True, has_finished_payment=True))





        # BEGIN Paginator
        # paginator = Paginator(place_list, 6)
        # page = request.GET.get('page')
        # places = paginator.get_page(page)
        
        # places.paginator.place_range = [item+1 for item in range(places.paginator.num_pages)]
        # context["place_list"] = places_pk
        # context["place_list_dict"] = places.paginator.__dict__
        # END Paginator


        # Left Panel
        context["place_additional_information"] = get_additional_information_important_attributes()
        capacity = request.GET.get("capacity")
        buffet = request.GET.get("buffet")
        date = request.GET.get("date")
        context["buffet"] = buffet
        context["date"] = date






        # filter
        place_list = sorted(filter_place_information(place_list_not_filtered, capacity, buffet, date), key=lambda k: k['feature'], reverse=True) 


        print("aaaaaa")
        print("aaaaaa")
        print("aaaaaa")
        print("aaaaaa")
        print("aaaaaa")
        print("aaaaaa")
        print("aaaaaa")
        print(place_list)
        places_pk = []
        for place in place_list:
            places_pk.append(place["pk"])
        context["places_pk"] = places_pk
        

        # Capacity
        if capacity == "":
            context["capacity"] = 0
            context["capacity_exists"] = True
        else:
            if float(capacity) > 500:
                context["capacity"] = "500+"
            else:
                context["capacity"] = capacity

        return render(request, "place_list.html", context)




class DetailPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["has_finished_payment"] = buyer_can_purchase(context)
        place_obj = Place.objects.get(pk=request.GET["pk"])

        # Place Visualization
        now = datetime.now()
        PlaceVisualization.objects.create(place=place_obj, creation=now)

        place = place_obj.__dict__
        place["children_rides"] = ast.literal_eval(str(place["children_rides"]).replace('"',""))
        place["decoration"] = ast.literal_eval(str(place["decoration"]).replace('"',""))
        context["place_seller"] = place_obj.sellerprofile.__dict__
        context["place"] = place
        context["place_capacity"] = place["capacity"]
        context["place_pk"] = place_obj.pk
        context["place_obj"] = place_obj

        # PHOTOs Detail
        photo_first = str(PlacePhoto.objects.filter(place=place_obj, is_first=True)[0].photo.photo)
        context["photo_list_html"] = [str(photo.photo.photo) for photo in PlacePhoto.objects.filter(place=place_obj, is_first=False)]
        context["photo_list_html"].insert(0, photo_first)


        context["photo_list_js"] = json.dumps(context["photo_list_html"], cls=DjangoJSONEncoder)

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

        if context["user_type"] != "anonymous":
            context["is_loved"] = PlaceLove.objects.filter(place=place_obj, user=request.user).exists()


        context["price_list"] = PlacePrice.objects.filter(place=place_obj)













        return render(request, "place_detail.html", context)



