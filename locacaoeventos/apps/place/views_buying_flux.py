from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic import View

from datetime import datetime
import ast, pagarme, json

from locacaoeventos.utils.main import *
from locacaoeventos.utils.general import *
from locacaoeventos.utils.place import *
from .placecore.models import Place, PlacePhoto
from .placereservation.models import PlacePrice, PlaceUnavailability, PlaceReservation, PlacePrice
from locacaoeventos.apps.user.sellerprofile.models import SellerProfile









class BuyPlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        capacity = request.GET.get("capacidade")
        context["capacity"] = capacity
        place_pk = request.GET.get("place_pk")
        date = ast.literal_eval(request.GET.get("date").replace(" ",""))
        context["date"] = date
        context["day"] = date[0]
        context["month"] = date[1]
        context["year"] = int(date[2])
        place = Place.objects.get(pk=place_pk)
        date = datetime.strptime(date[0] + date[1] + date[2], "%d%m%Y")

        period = ast.literal_eval("[" + request.GET.get("period") + "]")
        context["period"] = period
        if period == [1,0]:
            context["begin"] = place.period_soon_begin
            context["end"] = place.period_soon_end

        elif period == [0,1]:
            context["begin"] = place.period_late_begin
            context["end"] = place.period_late_end



        context["place_pk"] = request.GET.get("place_pk")

        placeprices = get_placeprices(place)

        placeprice_list = []
        for placeprice in placeprices:
            if int(capacity) <= int(placeprice["capacity_max"])+50 and int(capacity) >= int(placeprice["capacity_min"])-50:
                placeprice_list.append(placeprice)
            placeprice["final_value"] = int(capacity) * int(placeprice["value"])
            if int(placeprice["value_min"]) > placeprice["final_value"]:
                placeprice["final_value"] = placeprice["value_min"]
            placeprice["final_value_per_person"] = placeprice["final_value"]/int(capacity)
            
        if len(placeprice_list) == 0:
            context["placeprices_none"] = True

            for placeprice in placeprices:
                placeprice_list.append(placeprice)

        context["placeprices"] = placeprice_list
        context["place"] = get_single_place_dic(place)
        context["place_pk"] = place.pk
        print
        context["needs_js_input_fix"] = True

        # PAGARME
        context["encryption_key"] = settings.PAGARME_ENCRYPTION_KEY
        return render(request, "place_buy.html", context)



















class PurchasePlace(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        capacity = request.GET.get("capacidade")
        date = ast.literal_eval(request.GET.get("date"))
        period = ast.literal_eval("[" + request.GET.get("period") + "]")
        placeprice_pk = request.GET.get("placeprice_pk")
        place_pk = request.GET.get("place_pk")
        data = json.loads(request.GET.get("data"))

        place = Place.objects.get(pk=place_pk)
        seller = place.sellerprofile

        buyer = context["buyer"]
        birthday = buyer.birthday

        placeprice = PlacePrice.objects.get(pk=placeprice_pk)
        pagarme.authentication_key(settings.PAGARME_API_KEY)









        # Billing
        zip_code = request.GET.get("zip_code").replace("-", "")
        number = request.GET.get("number")
        state = request.GET.get("state")
        city = request.GET.get("city")
        neighbourhood = request.GET.get("neighbourhood")
        street = request.GET.get("street")








        # Faz a Transação
        params = {
            "amount": data["amount"],
            "card_hash": data["card_hash"],
            "installments":data["installments"],
            "customer": {
                "external_id": str(buyer.pk),
                "name": buyer.name,
                "type": "individual",
                "country": "br",
                "email": buyer.email,
                "documents": [
                    {
                        "type": "cpf",
                        "number": buyer.cpf.replace(".", "").replace("-", "")
                    }
                ],
                "phone_numbers": ["+" + buyer.cellphone.replace("(", "").replace(")", "").replace("-", "")],
                "birthday": str(birthday.year) + "-" + add_left_zero(str(birthday.month)) + "-" + str(birthday.day)
            },
            "billing": {
                "name": buyer.name,
                "address": {
                    "country": "br",
                    "state": state,
                    "city": city,
                    "neighborhood": neighbourhood,
                    "street": street,
                    "street_number": number,
                    "zipcode": zip_code
                }
            },
            "items": [
                {
                    "id": str(placeprice.pk),
                    "title": "EXEMPLO",
                    "unit_price": data["amount"],
                    "quantity": "1",
                    "tangible": False
                }
            ],
            "split_rules": [
                {
                    "recipient_id": seller.pagarme_id,
                    "percentage": "100",
                    "liable": True,
                    "charge_processing_fee": True
                }
            ]
        }
        trx = pagarme.transaction.create(params)


        if period == [0,1]:
            period = "max"
        else:
            period = "min"
        
        unavailability = PlaceUnavailability.objects.create(
            place=place,
            period=period,
            day=date[2] + "-" + date[1] + "-" + date[0],
        )  

        PlaceReservation.objects.create(
            place=place,
            placeprice=placeprice,
            buyer=buyer,
            unavailability=unavailability,
            creation=datetime.now(),
        )
















        





        context["encryption_key"] = settings.PAGARME_ENCRYPTION_KEY

        return render(request, "place_purchase.html", context)


    def post(self, request, *args, **kwargs):
        pagarme.authentication_key(settings.PAGARME_API_KEY)



        trx = pagarme.transaction.create(params)



        return render(request, "place_purchase.html", context)

