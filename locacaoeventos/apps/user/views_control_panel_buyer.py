import datetime, pytz
import pagarme

from django.views.generic import View
from django.shortcuts import render, redirect
from django.conf import settings

from locacaoeventos.utils.main import *
from locacaoeventos.utils.datetime import *
from locacaoeventos.utils.place import *
from locacaoeventos.utils.user import *

from .forms_user import *

from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto
from locacaoeventos.apps.place.placereservation.models import PlaceReservation, PlaceUnavailability
from locacaoeventos.apps.place.placereview.models import PlaceReview

from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile, FamilyMember

class EditBuyer(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "user"
        context["basemenu"] = "myaccount"
        context["has_finished_payment"] = buyer_can_purchase(context)
        buyer = context["buyer"]
        initial = {
            "name": buyer.name,
            "password": "aaaa",
            "cellphone": buyer.cellphone,
            "gender": buyer.gender,
            "civil_status": buyer.civil_status,
            "photo": buyer.photo,
            "cpf_buyer": buyer.cpf,
        }

        if buyer.birthday != None:
            initial["day"] = buyer.birthday.day
            initial["month"] = buyer.birthday.month
            initial["year"] = buyer.birthday.year

        context["form"] = BuyerForm(initial=initial, field_order = ['name'])

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
        buyer.cpf = form.cleaned_data["cpf_buyer"]
        buyer.gender = form.cleaned_data["gender"]
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
            if day != "" and month != "" and year != "":
                birthday = year + "-" + month + "-" + day
            else:
                birthday = None
            buyer.birthday = birthday

        else:
            context["is_valid_date"] = False


        buyer.save()



        if buyer.photo:
            context["buyer_photo_str"] = str(str(buyer.photo).replace("buyerprofile/photo/",""))
            context["buyer_photo"] = buyer.photo
        context["has_finished_payment"] = buyer_can_purchase(context)
        
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
                "description": place.description,
                "address": place.address,
            }

            photo = PlacePhoto.objects.filter(place=place, is_first=True)
            if photo:
                place_dic["photo"] = photo[0].photo.photo

            reviews_dic = get_reviews_from_place(place)
            place_dic["review_list"] = reviews_dic["review_list"]
            place_dic["review_rates"] = reviews_dic["review_rates"]
            

            day = reservation.unavailability.day
            utc = pytz.UTC
            if day < datetime.datetime.now().date():
                place_dic["has_passed"] = True
            place_dic["day"] = reservation.unavailability.day

            place_dic["canceled"] = reservation.canceled

            place_dic["can_cancel"] = get_can_cancel(reservation, place)[0]
            # Debug
            place_dic["days_before_event"] = get_can_cancel(reservation, place)[1]
            place_dic["hours_after_creating_reservation"] = get_can_cancel(reservation, place)[2]
            place_dic["place_reservation_price"] = get_can_cancel(reservation, place)[3]

            place_list.append(place_dic)
        place_list = sorted(place_list, key=lambda k: k['day'], reverse=True) 
        context["place_list"] = place_list
        context["can_refund"] = True

        return render(request, "control_panel/buyer_buffet_bought.html", context)





 
class CancelPlaceReservation(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["placereservation_pk"] = request.GET.get("placereservation_pk")
        context["place_refund"] = request.GET.get("place_refund")

        return render(request, "control_panel/buyer_placereservation_cancelled.html", context)

class CancelPlaceReservationConfirmed(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        # =========== BEGIN REFUND
        placereservation_pk = request.GET.get("placereservation_pk")
        place_refund = request.GET.get("place_refund")

        placereservation = PlaceReservation.objects.get(pk=placereservation_pk)
        reservation = placereservation
        place = placereservation.place
        pagarme_transaction = placereservation.pagarme_transaction
        pagarme.authentication_key(settings.PAGARME_API_KEY)
        trx = pagarme.transaction.find_by({
          'id': pagarme_transaction
        })[0]
        # print(trx)

        print()
        print()
        print()
        cancellation_policy = place.cancellation_policy
        print('cancellation_policy', cancellation_policy)

        days_before_event = (reservation.unavailability.day - datetime.datetime.today().date()).days
        print('days_before_event', days_before_event)

        hours_after_creating_reservation = (datetime.datetime.today().replace(tzinfo=None) - reservation.creation.replace(tzinfo=None)).total_seconds()/60/60
        print('hours_after_creating_reservation', hours_after_creating_reservation)

        place_reservation_price = reservation.value
        print('place_reservation_price', place_reservation_price)

        refund = False
        if cancellation_policy == "flexivel":
            # flexivel
            # Cancelamento até 48 horas após fazer a reserva e até 7 dias antes do evento, após este período pagamento integral do valor da reserva.
            if hours_after_creating_reservation < 48 and days_before_event < 7:
                refund = 1
        elif cancellation_policy == "moderada":
            # moderada
            # Cancelamento até 48 horas após fazer a reserva e até 14 dias antes do evento, após este período pagamento integral do valor da reserva.
            if hours_after_creating_reservation < 48 and days_before_event < 14:
                refund = 1
        elif cancellation_policy == "rigorosa":
            # rigorosa
            # 50% do reembolso caso o cancelamento ocorra ate 48 horas após fazer a reserva e até 21 dias antes do evento, após este período pagamento integral do valor da reserva.
            if hours_after_creating_reservation < 48 and days_before_event < 21:
                refund = 0.5





        amount = trx["authorized_amount"]
        refunded = trx["refunded_amount"]

        print(amount)
        print(refunded)

        if refund == 1:
            if amount != refunded:
                params_refund = {
                    'amount': amount-refunded
                }
        else:
            if refunded < amount/2:
                params_refund = {
                    'amount': amount/2-refunded
                }


        refunded_trx = pagarme.transaction.refund(trx['id'], params_refund)
        # =========== END REFUND

        placereservation.canceled = True
        placereservation.save()
        return render(request, "control_panel/buyer_placereservation_cancelled_confirmed.html", context)
























class ReviewPlaceBought(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "listbought"
        context["basemenu"] = "listbought"

        reservation_pk = request.GET.get("reservation")
        context_review_placebought(reservation_pk, context, request)

        return render(request, "control_panel/buyer_buffet_review.html", context)
    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["panel_type"] = "listbought"
        context["basemenu"] = "listbought"

        reservation_pk = request.POST.get("reservation_pk")
        context_review_placebought(reservation_pk, context, request)
        buyerprofile = context["buyer"]

        reservation = PlaceReservation.objects.get(pk=reservation_pk)
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





def context_review_placebought(reservation_pk, context, request):
    buyerprofile = context["buyer"]
    reservation = PlaceReservation.objects.get(pk=reservation_pk)
    place = reservation.unavailability.place
    context["place"] = {
        "pk": place.pk,
        "reservation_pk": reservation.pk,
        "name": place.name,
        "capacity": int(place.capacity),
        "description": place.description,
        "address": place.address,
        "photo": PlacePhoto.objects.filter(place=place)[0].photo.photo,
        "day": reservation.unavailability.day,
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













class FamilyBuyer(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context = context_familybuyer(context, request)
        context["form"] = FamilyMemberForm()

        return render(request, "control_panel/buyer_family.html", context)
    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        context = context_familybuyer(context, request)

        form = FamilyMemberForm(request.POST)
        buyer = BuyerProfile.objects.get(user=request.user)
        
        if form.is_valid():
            birthday = str(form.cleaned_data["year"]) + "-" + str(form.cleaned_data["month"]) + "-" + str(form.cleaned_data["day"])
            familymember = FamilyMember.objects.create(
                name=form.cleaned_data["name"],
                gender=form.cleaned_data["gender"],
                birthday=birthday,
                relation=form.cleaned_data["relation"],
                related_to=buyer,
            )
            context["form"] = FamilyMemberForm()
        else:
            context["form"] = FamilyMemberForm(request.POST)
            context["is_valid_date"] = False

        return render(request, "control_panel/buyer_family.html", context)


def context_familybuyer(context, request):
    context["panel_type"] = "family_member"
    context["basemenu"] = "family_member"

    related_to = BuyerProfile.objects.get(user=request.user)
    context["familymembers"] = FamilyMember.objects.filter(related_to=related_to)

    return context