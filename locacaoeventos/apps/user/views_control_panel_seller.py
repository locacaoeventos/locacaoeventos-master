from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import JsonResponse

import re, datetime, ast, pytz

from locacaoeventos.utils.buyingflux import *
from locacaoeventos.utils.datetime import *
from locacaoeventos.utils.main import *
from locacaoeventos.utils.place import *
from .forms_place import *
from .forms_user import *

from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto, PlaceAdditionalInformation, PhotoProvisory
from locacaoeventos.apps.place.placereservation.models import PlaceUnavailability, PlaceReservation, PlacePrice

# =========================================================
# EDIT SELLER
# =========================================================
class EditSeller(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context = context_editseller(request, context)
        seller = context["seller"]
        context["form"] = SellerForm(initial={
            "bank_code": seller.bank_code,
            "agency": seller.agency,
            "account": seller.account,
            "account_type": seller.account_type,


            "email_seller": seller.email,
            "name_seller": seller.name,
            "password_seller": "aaaa",
            "cpf": seller.cpf,
            "cnpj": seller.cnpj,
            "cellphone_seller": seller.cellphone,
            "name_seller": seller.name,
            "accepts_newsletter_seller": seller.accepts_newsletter
        })
        has_finished_payment = check_seller_has_finished_payment(
            seller_pk = seller.pk,
            bank_code = None,
            agency = None,
            account = None,
            account_type = None,
        )
        context["has_finished_payment"] = has_finished_payment[0]
        return render(request, "control_panel/seller_user_edit.html", context)


    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        context = context_editseller(request, context)
        seller = context["seller"]

        form = SellerForm(request.POST)
        form.is_valid()
        has_finished_payment = check_seller_has_finished_payment(
            seller_pk = seller.pk,
            bank_code = form.cleaned_data["bank_code"],
            agency = form.cleaned_data["agency"],
            account = form.cleaned_data["account"],
            account_type = form.cleaned_data["account_type"],
        )

        seller.has_finished_payment = has_finished_payment[0]

        seller.pagarme_id = has_finished_payment[1]
        seller.bank_code = form.cleaned_data["bank_code"]
        seller.agency = form.cleaned_data["agency"]
        seller.account = form.cleaned_data["account"]
        seller.account_type = form.cleaned_data["account_type"]

        seller.name = form.cleaned_data["name_seller"]
        seller.cpf = form.cleaned_data["cpf"]
        seller.cnpj = form.cleaned_data["cnpj"]
        seller.cellphone = form.cleaned_data["cellphone_seller"]
        


        if "accepts_newsletter_seller" in form.cleaned_data:
            seller.accepts_newsletter = True
            context["form"] = SellerForm(request.POST, initial={"accepts_newsletter_seller": True})
        else:
            seller.accepts_newsletter = False
            context["form"] = SellerForm(request.POST, initial={"accepts_newsletter_seller": False})

        if "password_seller" in form.cleaned_data:
            seller.user.set_password(form.cleaned_data["password_seller"])
            seller.user.save()
        seller.save()

        context["has_finished_payment"] = has_finished_payment[0]
        return render(request, "control_panel/seller_user_edit.html", context)


def context_editseller(request, context):
    context["panel_type"] = "user"
    context["basemenu"] = "myaccount"
    context["bank_code"] = get_bank_codes()
    context["account_type"] = get_account_types()
    
    return context




# =========================================================
# LIST OWNED
# =========================================================
class ListPlaceOwned(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "listowned"
        context["basemenu"] = "myaccount"
        context["has_finished_payment"] = context["seller"].has_finished_payment
        place_list = []
        for place in Place.objects.filter(sellerprofile=context["seller"]):
            place_dic = {
                "pk": place.pk,
                "name": place.name,
                "address": place.address,
                "description": place.description,
                "capacity": place.capacity,
                "creation": place.creation,
                "modified": place.modified,

                "is_active": place.is_active,
                "has_finished_basic": place.has_finished_basic,
            }

            photo = PlacePhoto.objects.filter(place=place, is_first=True)
            if photo:
                place_dic["photo"] = photo[0].photo.photo

            place_list.append(place_dic)
            reviews_dic = get_reviews_from_place(place)
            place_dic["review_list"] = reviews_dic["review_list"]
            place_dic["review_rates"] = reviews_dic["review_rates"]

            count_reservation = 0
            total_profit = 0
            for placereservation in PlaceReservation.objects.filter(place=place):
                total_profit += placereservation.placeprice.value
                count_reservation += 1
            place_dic["total_profit"] = "%.2f"%total_profit
            place_dic["count_reservation"] = count_reservation
        place_list = sorted(place_list, key=lambda k: k['modified'], reverse=True) 
        context["place_list"] = place_list
        return render(request, "control_panel/seller_place_list_owned.html", context)

























# =========================================================
# AVAILABILITY
# =========================================================
class AvailabilityPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        place_pk = request.GET.get("pk")
        context = context_availabilityplace(request, context, place_pk)
        return render(request, "control_panel/seller_place_availability.html", context)

    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        place_pk = request.POST.get("place_pk")
        place = Place.objects.get(pk=place_pk)

        soon_begin = request.POST.get("soon_begin")
        if soon_begin:
            soon_begin = convert_to_time(soon_begin)
            soon_end = request.POST.get("soon_end")
            if soon_end:
                soon_end = convert_to_time(soon_end)

                if soon_end > soon_begin:
                    place.period_soon_end = soon_end
                    place.period_soon_begin = soon_begin
                else:
                    place.period_soon_end = soon_begin
                    place.period_soon_begin = soon_end

        late_begin = request.POST.get("late_begin")
        late_end = request.POST.get("late_end")
        if late_begin or late_end:
            if late_begin and late_end:
                late_end = convert_to_time(late_end)
                late_begin = convert_to_time(late_begin)

                if late_end > late_begin:
                    place.period_late_end = late_end
                    place.period_late_begin = late_begin
                else:
                    place.period_late_end = late_begin
                    place.period_late_begin = late_end


            else:
                place.period_late_end = None
                place.period_late_begin = None


        else:
            place.period_late_end = None
            place.period_late_begin = None

        place.save()

        context = context_availabilityplace(request, context, place_pk)
        return render(request, "control_panel/seller_place_availability.html", context)


def context_availabilityplace(request, context, place_pk):
    context["panel_type"] = "listowned"
    context["basemenu"] = "myaccount"
    context["place_pk"] = place_pk
    place = Place.objects.get(pk=place_pk)
    context["place"] = place

    # Unavailabilites
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


    # Periods
    if place.period_soon_begin:
        context["soon_begin"] = convert_time_to_string(place.period_soon_begin)
    if place.period_soon_end:
        context["soon_end"] = convert_time_to_string(place.period_soon_end)
    if place.period_late_begin:
        context["late_begin"] = convert_time_to_string(place.period_late_begin)
    if place.period_late_end:
        context["late_end"] = convert_time_to_string(place.period_late_end)

    if place.period_soon_begin and place.period_soon_end:
        context["has_period"] = True


    # Price
    if PlacePrice.objects.filter(place=place):
        context["placeprice_list"] = True
    return context

















class UnavailabilityCreateAjax(View):
    def get(self, request, *args, **kwargs):
        data = {}

        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)
        day = request.GET.get("day").replace(" / ", "-")
        id_min_period = request.GET.get("id_min_period")
        id_max_period = request.GET.get("id_max_period")


        unavailability_repeat = request.GET.get("unavailability_repeat")
        if unavailability_repeat == "":
            unavailability_repeat = None



        # Checking if Date Exists
        error = False
        try:
            day = datetime.datetime.strptime(day, '%d-%m-%Y').date()
        except:
            error = "A data está inválida"

        # Checking if begin is sooner than today
        if not error:
            if day <= datetime.datetime.today().date():
                error = "A data está antes de agora"
        # All completed
        if not error:
            # Create Unavailability
            placeunavailability = PlaceUnavailability.objects.create(
                place=place,
                period="min",
                day=day,
                repeat=unavailability_repeat
            )
            placeunavailability = PlaceUnavailability.objects.create(
                place=place,
                period="max",
                day=day,
                repeat=unavailability_repeat

            )
        data["error"] = error
        data["place_pk"] = place_pk
        return JsonResponse(data)

























# =========================================================
# CREATE & EDIT
# =========================================================
class CreateEditPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["has_finished_payment"] = context["seller"].has_finished_payment
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
                photo_first = PlacePhoto.objects.filter(place=place, is_first=True)[0].photo
                photo_first_pk = photo_first.pk
                photo_first_src = photo_first.photo
                photos = [item.photo.pk for item in PlacePhoto.objects.filter(place=place) if item.is_first != True]
                photos.insert(0, photo_first_pk)
                # photos = [item.photo.pk for item in PlacePhoto.objects.filter(place=place)]
                context["form"] = PlaceForm(initial={
                    "name": place.name,
                    "address": place.address,
                    "description": place.description,
                    "capacity": place.capacity,
                    "video": place.video,
                    "children_rides": place.children_rides,
                    "decoration": place.decoration,
                    "menu": place.menu,
                    "photos": photos,
                    "first_photo": photo_first_pk,
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
                context["photo_first_src"] = photo_first_src
                context["menu_url"] = str(place.menu).replace("place/menu/", "")
            else:
                context["form"] = PlaceForm()
        else:
            context["form"] = PlaceForm()
        return render(request, "control_panel/seller_place_createedit.html", context)
    def post(self, request):
        context = base_context(request.user)
        context["has_finished_payment"] = context["seller"].has_finished_payment
        context["panel_type"] = "newplace"
        form = PlaceForm(self.request.POST, request.FILES)
        context["form"] = form
        place_pk = request.POST.get("place_pk", None)
        if place_pk:
            context["place_pk"] = place_pk
        if form.is_valid():
            # Video
            video = form.cleaned_data["video"].replace('/watch?v=', '/embed/')
            if "http" not in video and video != "":
                video = "https://" + video
            # Coordinates
            coordinates = get_latlng_from_address_str(form.cleaned_data["address"])
            # coordinates = [-23.5500827, -46.6540044]
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
                place.video = video
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
                first_photo = form.cleaned_data["first_photo"]
                PlacePhoto.objects.filter(place=place).delete() # Deleting current dependencies, to create new ones
                for i in range(len(photos)):
                    photo = PhotoProvisory.objects.get(pk=photos[i])
                    if photo.pk == first_photo:
                        PlacePhoto.objects.create(
                            place=place,
                            photo=photo,
                            is_first=True,
                        )
                    else:
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
                    video=video,
                    children_rides=children_rides,
                    decoration=decoration,
                    menu=menu,
                    sellerprofile=context["seller"],
                    lat=coordinates[0],
                    lng=coordinates[1],
                    has_finished_basic=False
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
                first_photo = form.cleaned_data["first_photo"]
                for i in range(len(photos)):
                    photo = PhotoProvisory.objects.get(pk=photos[i])
                    if photo.pk == first_photo:
                        PlacePhoto.objects.create(
                            place=place,
                            photo=photo,
                            is_first=True,
                        )
                    else:
                        PlacePhoto.objects.create(
                            place=place,
                            photo=photo
                        )

                context["place_pk"] = place.pk
                return render(request, "control_panel/seller_place_createedit_completed.html", context)
        return render(request, "control_panel/seller_place_createedit.html", context)

