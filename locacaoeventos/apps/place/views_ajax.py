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
            for i in range(len(additional_informations)):
                if getattr(placeadditionalinformation, additional_informations[i]) == False:
                    has_all = False
            if has_all:
                places.append(placeadditionalinformation.place)

        place_list = get_place_information(places)
        if len(place_list) > 0:
            data = { "place_list":place_list }
        else:
            data = { "none": "True" }
        return JsonResponse(data)









class OrderByBuffetAjax(View):
    def get(self, request, *args, **kwargs):



        # <option value="1">Relevância</option>
        # <option value="2">Preço - Maior</option>
        # <option value="3">Preço - Menor</option>
        # <option value="4">Avaliação - Maior</option>
        # <option value="5">Nome - A-Z</option>
        # <option value="6">Nome - Z-A</option>

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


            data = { "place_list":place_list_sorted }
        else:
            data = { "none": "True" }
        return JsonResponse(data)


