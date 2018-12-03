from django.views.generic import View
from django.http import JsonResponse

from locacaoeventos.apps.place.placecore.models import Place
from locacaoeventos.apps.place.placereservation.models import PlacePrice











def get_placeprice_list(place):
    placeprice_list = []
    for placeprice in PlacePrice.objects.filter(place=place):
        placeprice_dic = {
            "pk":placeprice.pk,
            "place_pk":placeprice.place.pk,
            "value":placeprice.value,
            "name":placeprice.name,
            "description":placeprice.description,
            "capacity_min":placeprice.capacity_min,
            "capacity_max":placeprice.capacity_max,
        }
        placeprice_list.append(placeprice_dic)
    return placeprice_list



class PlacePriceGetAjax(View):
    def get(self, request, *args, **kwargs):
        data = {}
        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)


        # Price
        data["placeprice_list"] = get_placeprice_list(place)


        return JsonResponse(data)




class PlacePriceCreateAjax(View):
    def get(self, request, *args, **kwargs):
        data = {"check":"check"}
        place_pk = request.GET.get("place_pk")
        name = request.GET.get("name")
        description = request.GET.get("description")
        value = request.GET.get("value")

        capacity_1 = request.GET.get("capacity_min")
        capacity_2 = request.GET.get("capacity_max")
        if capacity_1 > capacity_2:
            capacity_max = capacity_1
            capacity_min = capacity_2
        else:
            capacity_max = capacity_2
            capacity_min = capacity_1

        place = Place.objects.get(pk=place_pk)
        place.has_finished_basic = True
        place.save()

        PlacePrice.objects.create(
            place=place,
            value=value,
            name=name,
            description=description,
            capacity_min=capacity_min,
            capacity_max=capacity_max,
        )


        # Price
        data["placeprice_list"] = get_placeprice_list(place)


        return JsonResponse(data)




class PlacePriceDeleteAjax(View):
    def get(self, request, *args, **kwargs):
        data = {}
        placeprice_pk = request.GET.get("placeprice_pk")
        placeprice = PlacePrice.objects.get(pk=placeprice_pk)
        placeprice.delete()

        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)

        placeprice_list = get_placeprice_list(place)
        data["placeprice_list"] = placeprice_list

        if len(placeprice_list) == 0:
            place.has_finished_basic = False
            place.save()
        return JsonResponse(data)