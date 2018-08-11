from django.views.generic import View
from django.shortcuts import render, redirect

from locacaoeventos.utils.main import *
from locacaoeventos.utils.datetime import *
from locacaoeventos.utils.place import *

from .forms_user import *

from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto
from locacaoeventos.apps.place.placereservation.models import PlaceReservation, PlaceUnavailability
from locacaoeventos.apps.place.placereview.models import PlaceReview


class EditBuyer(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "user"
        context["basemenu"] = "myaccount"
        buyer = context["buyer"]
        context["form"] = BuyerForm(initial={
            "name": buyer.name,
            "password": "aaaa",
            "day": buyer.birthday.day,
            "month": buyer.birthday.month,
            "year": buyer.birthday.year,
            "cellphone": buyer.cellphone,
            "gender": buyer.gender,
            "civil_status": buyer.civil_status,
            "photo": buyer.photo,
        }, field_order = ['name'])

        context["is_valid_date"] = True
        if buyer.photo:
            context["buyer_photo_str"] = str(str(buyer.photo).replace("buyerprofile/photo/",""))
            context["buyer_photo"] = buyer.photo

        return render(request, "control_panel/buyer_user_edit.html", context)
    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "user"
        context["basemenu"] = "myaccount"

        buyer = context["buyer"]
        form = BuyerForm(request.POST, request.FILES)
        form.is_valid()
        buyer.civil_status = form.cleaned_data["civil_status"]
        buyer.name = form.cleaned_data["name"]
        buyer.cellphone = form.cleaned_data["cellphone"]
        buyer.photo = form.cleaned_data["photo"]
        if "accepts_newsletter" in form.cleaned_data:
            buyer.accepts_newsletter = True
            context["form"] = BuyerForm(request.POST, initial={"accepts_newsletter": True}, field_order=['name'])
        else:
            buyer.accepts_newsletter = False
            context["form"] = BuyerForm(request.POST, initial={"accepts_newsletter": False}, field_order=['name'])

        if "password" in form.cleaned_data:
            buyer.user.set_password(form.cleaned_data["password"])
            buyer.user.save()
        context["buyer_photo_str"] = str(str(form.cleaned_data["photo"]).replace("buyerprofile/photo/",""))

        if "day" in form.cleaned_data:
            context["is_valid_date"] = True
            day = str(form.cleaned_data["day"])
            month = str(form.cleaned_data["month"])
            year = str(form.cleaned_data["year"])
            buyer.birthday = year + "-" + month + "-" + day

        else:
            context["is_valid_date"] = False


        buyer.save()



        if buyer.photo:
            context["buyer_photo_str"] = str(str(buyer.photo).replace("buyerprofile/photo/",""))
            context["buyer_photo"] = buyer.photo
        
        return render(request, "control_panel/buyer_user_edit.html", context)


class ListPlaceBought(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "listbought"
        context["basemenu"] = "listbought"

        buyer = context["buyer"]
        place_list = []
        for reservation in PlaceReservation.objects.filter(buyer=buyer):
            place = reservation.unavailability.place
            place_dic = {
                "pk": place.pk,
                "pk_reservation": reservation.pk,
                "name": place.name,
                "capacity": place.capacity,
                "size": place.size,
                "description": place.description,
                "address": place.address,
                "photo": PlacePhoto.objects.filter(place=place)[0].photo.photo,

                "datetime_begin": reservation.unavailability.datetime_begin,
            }


            placreview = PlaceReview.objects.filter(reservation=reservation, buyerprofile=buyer)
            if placreview.exists():
                placreview = placreview[0]
                review = {
                    "exists": True,
                    "rate_infraestructure": placreview.rate_infraestructure,
                    "rate_rides": placreview.rate_rides,
                    "rate_cost_benefit": placreview.rate_cost_benefit,
                    "rate_attendance": placreview.rate_attendance,
                    "rate_children_opinion": placreview.rate_children_opinion,
                }
                place_dic["review"] = review
            place_list.append(place_dic)
        context["place_list"] = place_list

        return render(request, "control_panel/buyer_buffet_bought.html", context)


























class ReviewPlaceBought(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "buffet_review"
        buyerprofile = context["buyer"]
        reservation_pk = request.GET.get("reservation")
        reservation = PlaceReservation.objects.get(pk=reservation_pk)
        place = reservation.unavailability.place
        context["place"] = {
            "pk": place.pk,
            "reservation_pk": reservation.pk,
            "name": place.name,
            "capacity": int(place.capacity),
            "size": int(place.size),
            "description": place.description,
            "address": place.address,
            "photo": PlacePhoto.objects.filter(place=place)[0].photo.photo,
            "datetime_begin": reservation.unavailability.datetime_begin,
            "datetime_end": reservation.unavailability.datetime_end,
        }

        review = PlaceReview.objects.filter(reservation=reservation, buyerprofile=buyerprofile)
        if review.exists():
            review = review[0]
            context["review"] = {
                "comment": review.comment,
                "rate_infraestructure": review.rate_infraestructure,
                "rate_rides": review.rate_rides,
                "rate_cost_benefit": review.rate_cost_benefit,
                "rate_attendance": review.rate_attendance,
                "rate_children_opinion": review.rate_children_opinion,
            }
        if request.GET.get("just_reviewed", None):
            context["just_reviewed"] = True



        reviews_dic = get_reviews_from_place(place)
        context["review_list"] = reviews_dic["review_list"]
        context["review_rates"] = reviews_dic["review_rates"]






        return render(request, "control_panel/buyer_buffet_review.html", context)
    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        reservation_pk = request.POST.get("reservation_pk")

        reservation = PlaceReservation.objects.get(pk=reservation_pk)
        buyerprofile = context["buyer"]

        comment = request.POST.get("comment")
        rate_infraestructure = request.POST.get("rate_infraestructure")
        rate_rides = request.POST.get("rate_rides")
        rate_cost_benefit = request.POST.get("rate_cost_benefit")
        rate_attendance = request.POST.get("rate_attendance")
        rate_children_opinion = request.POST.get("rate_children_opinion")

        review = PlaceReview.objects.filter(reservation=reservation, buyerprofile=buyerprofile)
        if review.exists():
            review = review[0]
            review.comment = comment
            review.rate_infraestructure = rate_infraestructure
            review.rate_rides = rate_rides
            review.rate_cost_benefit = rate_cost_benefit
            review.rate_attendance = rate_attendance
            review.rate_children_opinion = rate_children_opinion
            review.save()
        else:
            PlaceReview.objects.create(
                reservation = reservation,
                buyerprofile = buyerprofile,
                comment = comment,
                rate_infraestructure = rate_infraestructure,
                rate_rides = rate_rides,
                rate_cost_benefit = rate_cost_benefit,
                rate_attendance = rate_attendance,
                rate_children_opinion = rate_children_opinion,
            )




        return redirect("/usuario/avaliar-buffet/?reservation=" + reservation_pk + "&just_reviewed=True")

