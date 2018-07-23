from django.views.generic import View
from django.shortcuts import render, redirect

import re

from locacaoeventos.utils.main import *
from locacaoeventos.utils.place import *
from .forms_place import *

from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto, PlaceAdditionalInformation, PhotoProvisory



class EditSeller(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "user"
        context["basemenu"] = "myaccount"
        return render(request, "control_panel/seller_user_edit.html", context)




class ListPlaceOwned(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "listowned"
        context["basemenu"] = "myaccount"

        place_list = []
        for place in Place.objects.filter(sellerprofile=context["seller"]):
            place_dic = {
                "pk": place.pk,
                "name": place.name,
                "address": place.address,
                "description": place.description,
                "size": place.size,
                "capacity": place.capacity,
                "is_active": place.is_active,
                "photo": PlacePhoto.objects.filter(place=place)[0].photo.photo,
            }
            place_list.append(place_dic)
            reviews_dic = get_reviews_from_place(place)
            place_dic["review_list"] = reviews_dic["review_list"]
            place_dic["review_rates"] = reviews_dic["review_rates"]

        context["place_list"] = place_list





        return render(request, "control_panel/seller_place_list_owned.html", context)



class CreateEditPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "newplace"
        context["basemenu"] = "myaccount"

        seller = context["seller"]
        place_pk = request.GET.get("pk", None)
        if place_pk is not None:
            place = Place.objects.get(pk=place_pk)

            # Edit Mode
            if place.sellerprofile == seller:
                context["place_pk"] = place_pk
                context["is_editing"] = True
                context["panel_type"] = "listowned"
                additionalinformation = PlaceAdditionalInformation.objects.get(place=place)
                photos = [item.photo.pk for item in PlacePhoto.objects.filter(place=place)]
                context["form"] = PlaceForm(initial={
                    "name": place.name,
                    "address": place.address,
                    "description": place.description,
                    "capacity": place.capacity,
                    "size": place.size,
                    "video": place.video,
                    "children_rides": place.children_rides,
                    "decoration": place.decoration,
                    "menu": place.menu,

                    "photos": photos,

                    "alcoholic_drink": additionalinformation.alcoholic_drink,
                    "has_entertainment": additionalinformation.has_entertainment,
                    "has_thematicdecoration": additionalinformation.has_thematicdecoration,
                    "has_childrenrides": additionalinformation.has_childrenrides,
                    "has_costumes": additionalinformation.has_costumes,
                    "has_parking": additionalinformation.has_parking,
                    "has_externalarea": additionalinformation.has_externalarea,
                    "has_music": additionalinformation.has_music,
                    "has_illumination": additionalinformation.has_illumination,
                    "has_babychangingroom": additionalinformation.has_babychangingroom,
                })
                context["menu_url"] = str(place.menu).replace("place/menu/", "")
            else:
                context["form"] = PlaceForm()

        else:
            context["form"] = PlaceForm()
        return render(request, "control_panel/seller_place_createedit.html", context)

    def post(self, request):
        context = base_context(request.user)
        context["panel_type"] = "newplace"
        form = PlaceForm(self.request.POST, request.FILES)
        context["form"] = form

        place_pk = request.POST.get("place_pk", None)
        if place_pk:
            context["place_pk"] = place_pk
        if form.is_valid():
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            # Video
            video = form.cleaned_data["video"].replace('/watch?v=', '/embed/')
            video = re.sub(r'.*youtube', 'https://www.youtube', video)
            # Coordinates
            coordinates = get_latlng_from_address_str(form.cleaned_data["address"])
            # Children Rides
            children_rides = str(form.cleaned_data["children_rides"]).replace("[","").replace("]","")
            children_rides = "{" + children_rides + "}"
            # Decoration
            decoration = str(form.cleaned_data["decoration"]).replace("[","").replace("]","")
            decoration = "{" + decoration + "}"
            # Menu

            menu_hidden = request.POST.get("menu_hidden")
            menu_forms = form.cleaned_data["menu"]
            if menu_hidden != "":
                if menu_forms is not None:
                    menu = menu_forms
                else:
                    menu = menu_hidden
            else:
                menu = menu_forms
            


            # ================================ Edit Mode
            if place_pk is not None and place_pk != "":
                # Place
                place = Place.objects.get(pk=place_pk)
                place.name = form.cleaned_data["name"]
                place.address = form.cleaned_data["address"]
                place.description = form.cleaned_data["description"]

                place.capacity = form.cleaned_data["capacity"]
                place.size = form.cleaned_data["size"]
                place.video = form.cleaned_data["video"]
                place.children_rides = children_rides
                place.decoration = decoration
                place.menu = menu
                place.sellerprofile = context["seller"]
                place.lat = coordinates[0]
                place.lng = coordinates[1]

                place.save()

                # ===================== Additional Information
                placeadditionalinformation = PlaceAdditionalInformation.objects.get(place=place)
                
                placeadditionalinformation.alcoholic_drink = form.cleaned_data["alcoholic_drink"]
                placeadditionalinformation.has_entertainment = form.cleaned_data["has_entertainment"]
                placeadditionalinformation.has_thematicdecoration = form.cleaned_data["has_thematicdecoration"]
                placeadditionalinformation.has_childrenrides = form.cleaned_data["has_childrenrides"]
                placeadditionalinformation.has_costumes = form.cleaned_data["has_costumes"]
                placeadditionalinformation.has_parking = form.cleaned_data["has_parking"]
                placeadditionalinformation.has_externalarea = form.cleaned_data["has_externalarea"]
                placeadditionalinformation.has_music = form.cleaned_data["has_music"]
                placeadditionalinformation.has_illumination = form.cleaned_data["has_illumination"]
                placeadditionalinformation.has_babychangingroom = form.cleaned_data["has_babychangingroom"]

                placeadditionalinformation.save()

                # ===================== Photos
                photos = form.cleaned_data["photos"]
                for i in range(len(photos)):
                    photo = PhotoProvisory.objects.get(pk=photos[i])
                    PlacePhoto.objects.filter(place=place, photo=photo).delete()
                    PlacePhoto.objects.create(
                        place=place,
                        photo=photo
                    )

                return redirect("/usuario/anunciante/buffet/listar/")

            # ================================ Creation Mode
            else:
                # Place
                place = Place.objects.create(
                    name=form.cleaned_data["name"],
                    address=form.cleaned_data["address"],
                    description=form.cleaned_data["description"],

                    capacity=form.cleaned_data["capacity"],
                    size=form.cleaned_data["size"],
                    video=form.cleaned_data["video"],
                    children_rides=children_rides,
                    decoration=decoration,

                    menu=menu,

                    sellerprofile=context["seller"],
                    lat=coordinates[0],
                    lng=coordinates[1],
                )


                # ===================== Additional Information
                PlaceAdditionalInformation.objects.create(
                    place=place,
                    alcoholic_drink=form.cleaned_data["alcoholic_drink"],
                    has_entertainment=form.cleaned_data["has_entertainment"],
                    has_thematicdecoration=form.cleaned_data["has_thematicdecoration"],
                    has_childrenrides=form.cleaned_data["has_childrenrides"],
                    has_costumes=form.cleaned_data["has_costumes"],
                    has_parking=form.cleaned_data["has_parking"],
                    has_externalarea=form.cleaned_data["has_externalarea"],
                    has_music=form.cleaned_data["has_music"],
                    has_illumination=form.cleaned_data["has_illumination"],
                    has_babychangingroom=form.cleaned_data["has_babychangingroom"],
                )

                # ===================== Photos
                photos = form.cleaned_data["photos"]
                for i in range(len(photos)):
                    photo = PhotoProvisory.objects.get(pk=photos[i])
                    PlacePhoto.objects.create(
                        place=place,
                        photo=photo
                    )

                return render(request, "control_panel/seller_place_createedit_completed.html", context)
        return render(request, "control_panel/seller_place_createedit.html", context)

