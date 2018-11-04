from django.views.generic import View
from django.http import JsonResponse

import ast


from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto, PlaceAdditionalInformation
from locacaoeventos.utils.place import *


class ListBuffetAjax(View):
    def get(self, request, *args, **kwargs):
        pnleft = ast.literal_eval(request.GET.get("pnleft"))
        additional_informations = [info for info in pnleft["additional_informations"] if info != ""]
        option = int(request.GET.get("option"))



        # ================ Filter like Home (Capacity, Search, Date)
        places_by_search = filter_place_information(
            place_list_not_filtered=get_place_information(Place.objects.filter(is_active=True, has_finished_basic=True)),
            capacity=pnleft["capacity"],
            buffet=pnleft["search"],
            date=pnleft["date"]
        )



        # ================ Filter By Additional Information
        places_by_additionalinformation = []

        if len(additional_informations) == 0:
            places_by_additionalinformation = [place for place in places_by_search]
        else:
            for placeadditionalinformation in PlaceAdditionalInformation.objects.all():
                has_all = True
                if len(additional_informations) >= 1 and additional_informations[0] != "": # If there's additionalinfo to filter
                    for i in range(len(additional_informations)):
                        if getattr(placeadditionalinformation, additional_informations[i]) == False:
                            has_all = False
                    if has_all:
                        if get_dic_by_key(
                            listdic=places_by_search,
                            key="pk",
                            value=placeadditionalinformation.place.pk
                        ): # If additionalinfo's Place on the list
                            places_by_additionalinformation.append(get_single_place_dic(placeadditionalinformation.place))


        # ================ Converting into list PKs
        items_pk = []
        for place in places_by_additionalinformation:
            items_pk.append(place["pk"])


        # ================ Ordering
        items_pk = order_by(option, items_pk)


        return JsonResponse(items_pk)











class OrderByBuffetAjax(View):
    def get(self, request, *args, **kwargs):
        places_pk = ast.literal_eval(request.GET.get("places_pk"))
        option = int(request.GET.get("option"))
        data = order_by(option, places_pk)
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








