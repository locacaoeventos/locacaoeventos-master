from django.views.generic import View
from django.shortcuts import render, redirect

from locacaoeventos.utils.main import *
from locacaoeventos.utils.place import *
from .forms_place import *

from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto



class EditSeller(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "user"
        return render(request, "control_panel/seller_user_edit.html", context)




class ListPlaceOwned(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "listowned"

        place_list = []
        for place in Place.objects.filter(sellerprofile=context["seller"]):
            place_dic = {
                "name": place.name,
                "address": place.address,
                "description": place.description,
                "size": place.size,
                "capacity": place.capacity,
                "photo": PlacePhoto.objects.filter(place=place)[0].photo.photo,
            }
            place_list.append(place_dic)
            reviews_dic = get_reviews_from_place(place)
            place_dic["review_list"] = reviews_dic["review_list"]
            place_dic["review_rates"] = reviews_dic["review_rates"]

        context["place_list"] = place_list





        return render(request, "control_panel/seller_place_list_owned.html", context)



class CreatePlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "newplace"
        context["place_additional_information"] = [{
            "name": "Serve bebidas alcólicas",
            "html_name":"alcoholic_drink",
            "html_id":"id_alcoholic_drink"
        }, {
            "name": "Enterteinimento",
            "html_name":"has_entertainment",
            "html_id":"id_has_entertainment"
        }, {
            "name": "Decoração Temática",
            "html_name":"has_thematicdecoration",
            "html_id":"id_has_thematicdecoration"
        }, {
            "name": "Brinquedo pra Crianças",
            "html_name":"has_childrenrides",
            "html_id":"id_has_childrenrides"
        }, {
            "name": "Fantasias para os Atores",
            "html_name":"has_costumes",
            "html_id":"id_has_costumes"
        }, {
            "name": "Estacionamento",
            "html_name":"has_parking",
            "html_id":"id_has_parking"
        }, {
            "name": "Área externa",
            "html_name":"has_externalarea",
            "html_id":"id_has_externalarea"
        }, {
            "name": "Música",
            "html_name":"has_music",
            "html_id":"id_has_music"
        }, {
            "name": "Iluminação",
            "html_name":"has_illumination",
            "html_id":"id_has_illumination"
        }, {
            "name": "Fraldário",
            "html_name":"has_babychangingroom",
            "html_id":"id_has_babychangingroom"
        }]
        context["form"] = PlaceForm()
        return render(request, "control_panel/seller_place_create.html", context)

    def post(self, request):
        context = base_context(request.user)
        context["panel_type"] = "newplace"
        context["form"] = PlaceForm()
        form = PlaceForm(self.request.POST, request.FILES)

        print(form.is_valid())
        print(form.is_valid())

        if form.is_valid():
            print("===============")
            print("===============")
            print(form.cleaned_data["menu"])
        #     photo = form.save()
        return render(request, "control_panel/seller_place_create.html", context)

