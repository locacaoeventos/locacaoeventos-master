from django.views.generic import View
from django.http import JsonResponse

import datetime

from locacaoeventos.utils.datetime import unavailability_repeat

from locacaoeventos.apps.place.placecore.models import Place
from locacaoeventos.apps.place.placereservation.models import PlacePrice, PlaceUnavailability










def get_placeprice_list(place):
    placeprice_list = []
    for placeprice in PlacePrice.objects.filter(place=place):
        placeprice_dic = {
            "pk":placeprice.pk,
            "place_pk":placeprice.place.pk,
            "name":placeprice.name,
            "description":placeprice.description,
            "description_long":placeprice.description_long,
            "capacity_min":placeprice.capacity_min,
            "capacity_max":placeprice.capacity_max,
            "value":"{0:.2f}".format(placeprice.value),
            "value_min":"{0:.2f}".format(placeprice.value_min),
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
        description = str(request.GET.get("description").replace("[","").replace("]","").split(",")).replace("'", '"')
        description_long = request.GET.get("description_long")
        value = float(request.GET.get("value").replace(".", "").replace(",", ".").replace("R$", "").replace(" ", ""))
        value_min = float(request.GET.get("value_min").replace(".", "").replace(",", ".").replace("R$", "").replace(" ", ""))


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
            value_min=value_min,
            name=name,
            description=description,
            description_long=description_long,
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

























class UnavailabilityGetAjax(View):
    def get(self, request, *args, **kwargs):
        data = {"check":"check"}

        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)

        placeunavailabilities = []
        today = datetime.datetime.now().date()
        for placeunavailability in PlaceUnavailability.objects.filter(place=place):
            if placeunavailability.day > today:
                day = placeunavailability.day.strftime("%d/%m/%Y")
                place = placeunavailability.place
                dic = {
                    "day": day,
                    "day_datetime": placeunavailability.day,
                    "placeunavailability_pk": placeunavailability.pk,
                }

                if placeunavailability.period == "min":
                    period = place.period_soon_begin.strftime("%Hh%M") + " - " + place.period_soon_end.strftime("%Hh%M")
                elif placeunavailability.period == "max":
                    period = place.period_late_begin.strftime("%Hh%M") + " - " + place.period_late_end.strftime("%Hh%M")
                dic["period"] = period


                repeat = unavailability_repeat(placeunavailability.repeat)
                dic["repeat"] = repeat
                placeunavailabilities.append(dic)
        placeunavailabilities = sorted(placeunavailabilities, key=lambda k: k['day_datetime'], reverse=False) 
        data["placeunavailabilities"] = placeunavailabilities
        return JsonResponse(data)




class UnavailabilityDeleteAjax(View):
    def get(self, request, *args, **kwargs):
        data = {"check":"check"}

        placeunavailability_pk = request.GET.get("placeunavailability_pk")
        PlaceUnavailability.objects.get(pk=placeunavailability_pk).delete()
        return JsonResponse(data)

