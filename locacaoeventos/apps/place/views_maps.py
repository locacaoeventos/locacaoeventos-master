from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Case, When
from django.core.serializers.json import DjangoJSONEncoder

import json

from locacaoeventos.utils.main import *
from locacaoeventos.utils.place import *

from locacaoeventos.apps.place.views_ajax import ListBuffetAjax

from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto



class MapsPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["place_additional_information"] = get_additional_information_important_attributes()

        data_list = []
        for place in Place.objects.filter(is_active=True, has_finished_basic=True):
            data_dic = {
                "id": place.pk,
                "category": "real_estate",
                "title": place.name,
                "location": place.address,
                "latitude": place.lat,
                "longitude": place.lng,
                "url": "/buffet/detalhar/?pk=" + str(place.pk),
                "type": "Apartment",
                "type_icon": "/static/base_template_user/assets/icons/hotels/villa.png",
            }

            gallery = []
            for photo in PlacePhoto.objects.filter(place=place):
                gallery.append("/media/" + str(photo.photo.photo))

            data_dic["gallery"] = gallery

            place = get_single_place_dic(place)

            for i in range(len(place["review_list"]["review_list"])):
                place["review_list"]["review_list"][i]["buyerprofile"] = ""
                place["review_list"]["review_list"][i]["creation"] = ""

            data_dic["place"] = place
            data_list.append(data_dic)

        context["data"] = json.dumps(
            {"data": data_list},
            sort_keys=True,
            indent=1,
            cls=DjangoJSONEncoder
        )

        return render(request, "place_maps.html", context)





class MapsPlaceAjax(View):
    def get(self, request, *args, **kwargs):

        items_pk = json.loads(ListBuffetAjax.get(self, request, *args, **kwargs).content)["items_pk"]
        data_list = []


        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(items_pk)])




        for place in Place.objects.filter(pk__in=items_pk).order_by(preserved):
            data_dic = {
                "id": place.pk,
                "category": "real_estate",
                "title": place.name,
                "location": place.address,
                "latitude": place.lat,
                "longitude": place.lng,
                "url": "/buffet/detalhar/?pk=" + str(place.pk),
                "type": "Apartment",
                "type_icon": "/static/base_template_user/assets/icons/hotels/villa.png",
            }

            gallery = []
            for photo in PlacePhoto.objects.filter(place=place):
                gallery.append("/media/" + str(photo.photo.photo))

            data_dic["gallery"] = gallery

            place = get_single_place_dic(place)

            for i in range(len(place["review_list"]["review_list"])):
                place["review_list"]["review_list"][i]["buyerprofile"] = ""
                place["review_list"]["review_list"][i]["creation"] = ""

            data_dic["place"] = place
            data_list.append(data_dic)

        json.dumps({"data": data_list})

        return JsonResponse({"data": data_list})


