from django.views.generic import View
from django.http import JsonResponse

import ast


from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto, PlaceAdditionalInformation
from locacaoeventos.utils.place import *


class ListBuffetAjax(View):
    def get(self, request, *args, **kwargs):

        search = request.GET.get("search")
        date = request.GET.get("date")
        capacity = request.GET.get("capacity")


        data = {
        }
        return JsonResponse(data)


class ListBuffetAdditionalInformationAjax(View):
    def get(self, request, *args, **kwargs):
        additional_informations = request.GET.get("additional_informations").split(",")
        places = []
        for placeadditionalinformation in PlaceAdditionalInformation.objects.all():
            has_all = True
            if len(additional_informations) > 1:
                for i in range(len(additional_informations)):
                    if getattr(placeadditionalinformation, additional_informations[i]) == False:
                        has_all = False
                if has_all:
                    places.append(placeadditionalinformation.place)


        # Filter by Name/Location, Capacity and Date
        if len(additional_informations) == 1:
            places = [place for place in Place.objects.filter(is_active=True, has_finished_basic=True)]

        items_pk = []
        for place in places:
            items_pk.append(place.pk)
        if len(items_pk) > 0:
            data = { "items_pk":items_pk }
        else:
            data = { "none": "True" }
        return JsonResponse(data)









class OrderByBuffetAjax(View):
    def get(self, request, *args, **kwargs):


        current_pks = ast.literal_eval(request.GET.get("current_pks"))
        option = int(request.GET.get("option"))
        places = [Place.objects.get(pk=place_pk) for place_pk in current_pks]
        place_list = get_place_information(places)
        if len(place_list) > 0:
            for i in range(len(place_list)):
                place_list[i]["placeprice_min"] = float(place_list[i]["placeprice_min"])

            # =============================
            # Price
            # =============================
            if option == 2 or option == 3:
                if option == 2: # Bigger Price
                    place_list_sorted = sorted(place_list, key=lambda k: k['placeprice_min'], reverse=True) 
                elif option == 3: # Smaller Price
                    place_list_sorted = sorted(place_list, key=lambda k: k['placeprice_min']) 


            # =============================
            # Rate
            # =============================
            elif option == 4:
                place_list_sorted = []
                pk_list = []

                # Here, we ignore "Nones"
                for i in range(len(place_list)):
                    highest_rate = -1
                    pk_selected = None
                    print("==========", i)
                    for j in range(len(place_list)):
                        if place_list[j]["review_list"]["review_rates"] != "None":
                            rate_average = float(place_list[j]["review_list"]["review_rates"]["rate_average"])
                            if rate_average >= highest_rate:
                                if place_list[j]["pk"] not in pk_list:
                                    pk_selected = place_list[j]["pk"]
                                    highest_rate = rate_average
                                    print(highest_rate)

                    if pk_selected is not None:
                        for j in range(len(place_list)):
                            if place_list[j]["pk"] == pk_selected:
                                place_list_sorted.append(place_list[j])
                                pk_list.append(place_list[j]["pk"])


                # We add the nones
                if len(place_list) != len(place_list_sorted):
                    for i in range(len(place_list)):
                        if place_list[i]["review_list"]["review_rates"] == "None":
                            place_list_sorted.append(place_list[i])



            # =============================
            # Name
            # =============================
            elif option == 5 or option == 6:
                if option == 5: # A-Z
                    place_list_sorted = sorted(place_list, key=lambda k: k['name']) 
                elif option == 6: # Z-A
                    place_list_sorted = sorted(place_list, key=lambda k: k['name'], reverse=True) 


            for i in range(len(place_list_sorted)):
                place_list_sorted[i]["placeprice_min"] = "%.2f"%place_list_sorted[i]["placeprice_min"]

            items_pk = []
            for i in range(len(place_list_sorted)):
                items_pk.append(place_list_sorted[i]["pk"])

            data = { "items_pk":items_pk }
        else:
            data = { "none": "True" }
        return JsonResponse(data)







class GetPlaceInformation(View):
    def get(self, request, *args, **kwargs):
        try:
            items_pk = ast.literal_eval(request.GET.get("items_pk"))
            list_places_obj = []
            for i in range(len(items_pk)):
                place = Place.objects.get(pk=items_pk[i])
                list_places_obj.append(place)
            list_places = get_place_information(list_places_obj)

            data = { "list_places": list_places }
        except:
            data = { "none": True }
        return JsonResponse(data)








