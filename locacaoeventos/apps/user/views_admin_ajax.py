from django.views.generic import View
from django.http import HttpResponse
from django.http import JsonResponse

from locacaoeventos.apps.place.placecore.models import Place



class ListBuffetBan(View):
    def get(self, request, *args, **kwargs):
        place_pk = request.GET.get("pk")
        place = Place.objects.get(pk=place_pk)
        is_active = place.is_active
        if is_active:
            place.is_active = False
            is_active = False
        else:
            place.is_active = True
            is_active = True
        place.save()
        data = {
            "pk": request.GET.get("pk"),
            "is_active": is_active
        }
        return JsonResponse(data)




class VerifyBuffet(View):
    def get(self, request, *args, **kwargs):
        place_pk = request.GET.get("pk")
        is_authorized = str(request.GET.get("is_authorized"))
        place = Place.objects.get(pk=place_pk)
        if is_authorized == "True":
            place.is_authorized_by_admin = False
            is_authorized = False
        else:
            place.is_authorized_by_admin = True
            is_authorized = True
        place.save()
        data = {
            "pk": request.GET.get("pk"),
            "is_authorized": is_authorized
        }
        return JsonResponse(data)
