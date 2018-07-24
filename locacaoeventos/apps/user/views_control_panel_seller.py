from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

import re, datetime, ast, pytz

from locacaoeventos.utils.main import *
from locacaoeventos.utils.place import *
from .forms_place import *

from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto, PlaceAdditionalInformation, PhotoProvisory
from locacaoeventos.apps.place.placereservation.models import PlaceUnavailability, PlaceReservation

# =========================================================
# EDIT SELLER
# =========================================================
class EditSeller(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "user"
        context["basemenu"] = "myaccount"
        seller = context["seller"]
        context["form"] = SellerForm(initial={
            "email_seller": seller.email,
            "name": seller.name,
            "cpf": seller.cpf,
            "cnpj": seller.cnpj,
        })


        return render(request, "control_panel/seller_user_edit.html", context)












# =========================================================
# LIST OWNED
# =========================================================
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
                "creation": place.creation,
                "photo": PlacePhoto.objects.filter(place=place)[0].photo.photo,

                "is_active": place.is_active,
                "has_finished_basic": place.has_finished_basic,
            }
            place_list.append(place_dic)
            reviews_dic = get_reviews_from_place(place)
            place_dic["review_list"] = reviews_dic["review_list"]
            place_dic["review_rates"] = reviews_dic["review_rates"]
        place_list = sorted(place_list, key=lambda k: k['creation']) 
        context["place_list"] = place_list
        return render(request, "control_panel/seller_place_list_owned.html", context)

























# =========================================================
# AVAILABILITY
# =========================================================
class AvailabilityPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "listowned"
        context["basemenu"] = "myaccount"
        place_pk = request.GET.get("pk")
        context["place_pk"] = place_pk
        place = Place.objects.get(pk=place_pk)
        context["place"] = place
        unavailabilities = []
        unavailabilities_byus = []
        for placeunavailability in PlaceUnavailability.objects.filter(place=place):
            placereservation = PlaceReservation.objects.filter(unavailability=placeunavailability)
            if placereservation:
                unavailabilities_byus.append(placereservation[0])
            else:
                unavailabilities.append(placeunavailability)
        context["unavailabilities"] = unavailabilities
        context["unavailabilities_byus"] = unavailabilities_byus
        return render(request, "control_panel/seller_place_availability.html", context)


class UnavailabilityCreateAjax(View):
    def get(self, request, *args, **kwargs):
        data = {}
        unavailability_begin = request.GET.get("unavailability_begin").split(",")
        unavailability_end = request.GET.get("unavailability_end").split(",")
        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)
        utc = pytz.UTC
        datetime_begin = ""
        datetime_end = ""
        for i in range(len(unavailability_begin)):
            if i != 0:
                datetime_begin += "-" + str(unavailability_begin[i])
                datetime_end += "-" + str(unavailability_end[i])
            else:
                datetime_begin += str(unavailability_begin[i])
                datetime_end += str(unavailability_end[i])
        # Checking if Date Exists
        error = False
        try:
            datetime_begin = datetime.datetime.strptime(datetime_begin, '%d-%m-%Y-%H-%M')
            datetime_end = datetime.datetime.strptime(datetime_end, '%d-%m-%Y-%H-%M')
        except:
            data["error"] = "A data está inválida"
            error = True
        # Checking if end is after than begin
        if not error:
            if datetime_begin > datetime_end:
                data["error"] = "A data de fim está antes da data de começo"
                error = True
        # Checking if begin is sooner than today
        if not error:
            if datetime_begin < datetime.datetime.today():
                data["error"] = "A data está antes de agora"
                error = True
        # Checking if there's already unavailability on that period
        if not error:
            for unavailability in PlaceUnavailability.objects.filter(place=place):
                crossing_dates = True
                if datetime_begin.replace(tzinfo=utc) < unavailability.datetime_begin and datetime_end.replace(tzinfo=utc) < unavailability.datetime_end:
                    crossing_dates = False
                elif datetime_begin.replace(tzinfo=utc) > unavailability.datetime_begin and datetime_end.replace(tzinfo=utc) > unavailability.datetime_end:
                    crossing_dates = False
                if crossing_dates:
                    data["error"] = "Este horário já encontra-se ocupado"
                    error = True
        # Create Unavailability
        if not error:
            data["error"] = "false"
            placeunavailability = PlaceUnavailability.objects.create(
                place=place,
                datetime_begin=datetime_begin,
                datetime_end=datetime_end,
            )
            data["place_pk"] = place_pk
        return JsonResponse(data)




class UnavailabilityDetailAjax(View):
    def get(self, request, *args, **kwargs):
        data = {}

        pk = request.GET.get("pk")
        this_day = request.GET.get("this_day")
        datetime_this_day = datetime.datetime.strptime(this_day, '%Y-%m-%d')
        place = Place.objects.get(pk=pk)

        unavailability_this_day = []
        for unavailability in PlaceUnavailability.objects.filter(place=place):
            if unavailability.datetime_begin>datetime_this_day and unavailability.datetime_end<datetime_this_day:
                if unavailability.datetime_begin<datetime_this_day and unavailability.datetime_end>datetime_this_day:
                    unavailability_this_day.append("00h00-23h59")

                elif datetime_this_day<unavailability.datetime_begin:
                    unavailability_this_day.append("00h00-23h59")



        data["unavailability_this_day"] = unavailability_this_day
        return JsonResponse(data)

















# =========================================================
# CREATE & EDIT
# =========================================================
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
                    has_finished_basic=True
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

