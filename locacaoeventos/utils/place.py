from datetime import datetime
import pytz, math, ast

from locacaoeventos.utils.general import *

from locacaoeventos.apps.place.placereservation.models import PlaceReservation, PlaceUnavailability, PlacePrice
from locacaoeventos.apps.place.placereview.models import PlaceReview
from locacaoeventos.apps.place.placecore.models import PlacePhoto, Place
from locacaoeventos.apps.user.chat.models import Message

def get_reviews_from_place(place):
    response = {}
    review_list = []
    sum_rate_infraestructure = 0
    sum_rate_rides = 0
    sum_rate_cost_benefit = 0
    sum_rate_attendance = 0
    sum_rate_children_opinion = 0
    sum_rate_average = 0
    count_review = 0
    for unavailability in PlaceUnavailability.objects.filter(place=place):
        reservation = PlaceReservation.objects.filter(unavailability=unavailability)
        if reservation:
            reservation = reservation[0]
            review = PlaceReview.objects.filter(reservation=reservation)
            if review:
                review = review[0]
                review_list.append({
                    "buyerprofile": review.buyerprofile,
                    "creation": review.creation.date(),
                    "comment": review.comment,
                    "pk": review.pk,
                    "rate_infraestructure": review.rate_infraestructure,
                    "rate_rides": review.rate_rides,
                    "rate_cost_benefit": review.rate_cost_benefit,
                    "rate_attendance": review.rate_attendance,
                    "rate_children_opinion": review.rate_children_opinion,
                    "rate": str(review.get_average_rate()).replace(",", ".")
                })
                sum_rate_infraestructure += review.rate_infraestructure
                sum_rate_rides += review.rate_rides
                sum_rate_cost_benefit += review.rate_cost_benefit
                sum_rate_attendance += review.rate_attendance
                sum_rate_children_opinion += review.rate_children_opinion
                sum_rate_average += review.rate_infraestructure + review.rate_rides + review.rate_cost_benefit + review.rate_attendance + review.rate_children_opinion
                count_review += 1
    response["review_list"] = review_list
    if count_review != 0:
        response["review_rates"] = {
            "rate_infraestructure": str(math.floor(sum_rate_infraestructure/count_review*10)/10).replace(",", "."),
            "rate_rides": str(math.floor(sum_rate_rides/count_review*10)/10).replace(",", "."),
            "rate_cost_benefit": str(math.floor(sum_rate_cost_benefit/count_review*10)/10).replace(",", "."),
            "rate_attendance": str(math.floor(sum_rate_attendance/count_review*10)/10).replace(",", "."),
            "rate_children_opinion": str(math.floor(sum_rate_children_opinion/count_review*10)/10).replace(",", "."),
            "rate_average": str(math.floor(sum_rate_average/count_review/5*10)/10).replace(",", "."),
            "n_review": count_review
        }
    else:
        response["review_rates"] = "None"
    return response









def get_additional_information_important_attributes():
    additional_informations = [ # label_ordered = "Área" was put as last, 'cause it's special char
        {
            "name": "alcoholic_drink",
            "id_name": "id_alcoholic_drink",
            "label": "Serve bebidas alcólicas",
            "label_ordered": "Serve bebidas alcólicas"
        },
        {
            "name": "has_entertainment",
            "id_name": "id_has_entertainment",
            "label": "Entretenimento",
            "label_ordered": "Entretenimento"
        },
        {
            "name": "has_plays",
            "id_name": "id_has_plays",
            "label": "Gincanas",
            "label_ordered": "Gincanas"
        },
        {
            "name": "has_thematicdecoration",
            "id_name": "id_has_thematicdecoration",
            "label": "Decoração Temática",
            "label_ordered": "Decoração Temática"
        },
        {
            "name": "has_childrenrides",
            "id_name": "id_has_childrenrides",
            "label": "Brinquedo pra Crianças",
            "label_ordered": "Brinquedo pra Crianças"
        },
        {
            "name": "has_costumes",
            "id_name": "id_has_costumes",
            "label": "Fantasias para os Atores",
            "label_ordered": "Fantasias para os Atores"
        },
        {
            "name": "has_parking",
            "id_name": "id_has_parking",
            "label": "Estacionamento",
            "label_ordered": "Estacionamento"
        },
        {
            "name": "has_externalarea",
            "id_name": "id_has_externalarea",
            "label": "Área externa",
            "label_ordered": "Area externa"
        },
        {
            "name": "has_music",
            "id_name": "id_has_music",
            "label": "Música",
            "label_ordered": "Música"
        },
        {
            "name": "has_illumination",
            "id_name": "id_has_illumination",
            "label": "Iluminação",
            "label_ordered": "Iluminação"
        },
        {
            "name": "has_babychangingroom",
            "id_name": "id_has_babychangingroom",
            "label": "Fraldário",
            "label_ordered": "Fraldário"
        },
        {
            "name": "has_actors",
            "id_name": "id_has_actors",
            "label": "Animadores",
            "label_ordered": "Animadores"
        },
        {
            "name": "has_generator",
            "id_name": "id_has_generator",
            "label": "Gerador de energia",
            "label_ordered": "Gerador de energia"
        },
        {
            "name": "has_aircon",
            "id_name": "id_has_aircon",
            "label": "Ar Condicionado",
            "label_ordered": "Ar Condicionado"
        },
        {
            "name": "has_handicapped_acess",
            "id_name": "id_has_handicapped_acess",
            "label": "Acessível para deficientes",
            "label_ordered": "Acessível para deficientes"
        },
        {
            "name": "has_wifi",
            "id_name": "id_has_wifi",
            "label": "Wi-Fi",
            "label_ordered": "Wi-Fi"
        },
        {
            "name": "has_valet",
            "id_name": "id_has_valet",
            "label": "Manobrista e/ou valet",
            "label_ordered": "Manobrista e/ou valet"
        },
        {
            "name": "has_acoustics",
            "id_name": "id_has_acoustics",
            "label": "Isolamento acústico",
            "label_ordered": "Isolamento acústico"
        },
    ]
    additional_informations = sorted(additional_informations, key=lambda k: k['label_ordered']) 
    return additional_informations
























def get_messages_to_chat(user, is_seller):
    messages_from = [{
        "user_contacted": message.user_to,
        "text": message.text,
        "datetime": message.datetime,
        "place": message.place,
        } for message in Message.objects.filter(user_from=user)
    ]
    messages_to = [{
        "user_contacted": message.user_from,
        "text": message.text,
        "datetime": message.datetime,
        "place": message.place,
        } for message in Message.objects.filter(user_to=user)
    ]

    messages = messages_from + messages_to
    if is_seller == True:
        for message in messages:
            message["photo"] = BuyerProfile.objects.get(user=message["user_contacted"]).photo

    else:
        for message in messages:
            message["photo"] = PlacePhoto.objects.filter(place=message["place"], is_first=True)[0].photo

        
    messages = sorted(messages, key=lambda k: k['datetime'], reverse=True) 
    return messages










def get_single_place_dic(place):
    place_dic = {
        "pk": place.pk,
        "name": place.name,
        "description": place.description,
        "capacity": place.capacity,
        "address": place.address,
        "lat": place.lat,
        "lng": place.lng,
        "feature": place.feature,
        "period_soon_begin": place.period_soon_begin,
        "period_soon_end": place.period_soon_end,
        "period_late_begin": place.period_late_begin,
        "period_late_end": place.period_late_end,
    }
    place_dic["photo"] = str(PlacePhoto.objects.filter(place=place, is_first=True)[0].photo.photo)


    place_dic["placeprice_min"] = get_place_pricemin(place)
    review_list = get_reviews_from_place(place)
    for i in range(len(review_list["review_list"])):
        review_list["review_list"][i]["buyerprofile"] = review_list["review_list"][i]["buyerprofile"].pk
    place_dic["review_list"] = review_list
    return place_dic



def get_place_information(places):
    place_list = []
    for place in places:
        place_list.append(get_single_place_dic(place))
    return place_list








def get_place_pricemin(place):
    placeprice_min = 9999999999999
    for placeprice in PlacePrice.objects.filter(place=place):
        if placeprice.value < placeprice_min:
            placeprice_min = placeprice.value
    if placeprice_min != 9999999999999:
        placeprice_min = "%.2f"%placeprice_min
    return placeprice_min



def filter_place_information(place_list_not_filtered, capacity, buffet, date):
    place_list = []
    if capacity == "" and buffet == "" and date == "":
        print("MERDA1")
        return place_list_not_filtered
    else:
        print("DEU")
        if buffet != "":
            print("DEU2")
            print(buffet)
            try:
                latlng = get_latlng_from_address_str(buffet)
            except:
                latlng = None


            # Filter by Location
            if latlng is not None:
                lat_difference = 0.003
                lng_difference = 0.06

                lat = get_positive(latlng[0])
                lng = get_positive(latlng[1])

                for i in range(len(place_list_not_filtered)):
                    place = place_list_not_filtered[i]

                    lat_place = get_positive(place["lat"])
                    lng_place = get_positive(place["lng"])

                    if get_positive(lat_place - lat) <= lat_difference and get_positive(lng_place - lng) <= lng_difference:
                        place_list.append(place)

            # Filter by Name
            for i in range(len(place_list_not_filtered)):
                place = place_list_not_filtered[i]

                buffet_list_str = buffet.split(" ")
                for i in range(len(buffet_list_str)):
                    buffet_str = buffet_list_str[i]
                    break_loop = False
                    if len(buffet_str) > 2:
                        place_list_str = place["name"].split(" ")
                        for j in range(len(place_list_str)):
                            place_str = place_list_str[j].replace(",", "").replace("-", "")
                            if len(place_str) > 2:
                                if compare_strings(buffet_str, place_str):
                                    if get_dic_by_key(place_list, "pk", place["pk"]) is None:
                                        place_list.append(place)
                                        break_loop = True
                                        break
                    if break_loop:
                        break

        else:
            print("TESTE 1")
            place_list = place_list_not_filtered



        # Filter by Capacity
        if capacity != "" and capacity != "sem":
            print("TESTE 2")
            place_list_filtered_capacity = []


            for i in range(len(place_list)):
                place = place_list[i]
                if capacity == "500+":
                    capacity = 500

                capacity_tolerance = 50
                capacity = int(capacity)
                capacity_place = int(place["capacity"])

                if capacity+capacity_tolerance >= capacity_place and capacity-capacity_tolerance <= capacity_place:
                    place_list_filtered_capacity.append(place)
                elif capacity == 500 and capacity_place >= 500:
                    place_list_filtered_capacity.append(place)
                elif capacity == 0:
                    place_list_filtered_capacity.append(place)
        else:
            print("TESTE 3")
            place_list_filtered_capacity = place_list

        # Filter by Date
        place_list_filtered_date = []
        if date != "":
            print("TESTE 4")
            date_analyse_prep = date.replace(" ", "")
            date_analyse = datetime.strptime(date.replace(" ", "") + " 0", '%d/%m/%Y %H')
            day = date_analyse.day
            month = date_analyse.month
            year = date_analyse.year
            for i in range(len(place_list_filtered_capacity)):
                place_obj = Place.objects.get(pk=place_list_filtered_capacity[i]["pk"])
                place_dic = place_list_filtered_capacity[i]
                unavailabilities = PlaceUnavailability.objects.filter(place=place_obj)
                is_occupied = 0
                for unavailability in unavailabilities:
                    print("==============")
                    print(str(date_analyse.replace(tzinfo=pytz.UTC)).replace(" 00:00:00+00:00", ""))
                    print(str(unavailability.day))
                    if str(date_analyse.replace(tzinfo=pytz.UTC)).replace(" 00:00:00+00:00", "") == str(unavailability.day):
                        print("OCCUPY")
                        print("OCCUPY")
                        print("OCCUPY")
                        is_occupied += 1
                    # if date_analyse.replace(tzinfo=utc) > unavailability.datetime_begin.replace(tzinfo=utc) and date_analyse.replace(tzinfo=utc) < unavailability.datetime_end.replace(tzinfo=utc):
                    #     is_occupied = True
                
                if is_occupied < 2:
                    place_list_filtered_date.append(place_dic)


        return place_list_filtered_date



def get_placeprices(place):
    placeprices = []
    for placeprice in PlacePrice.objects.filter(place=place):
        placeprices.append({
            "pk": placeprice.pk,
            "value": placeprice.value,
            "value_min": placeprice.value_min,
            "name": placeprice.name,
            "description": ast.literal_eval(placeprice.description),
            "description_long": placeprice.description_long,
            "capacity_min": placeprice.capacity_min,
            "capacity_max": placeprice.capacity_max,

        })
    return placeprices



def order_by(option, places_pk):
    places = [Place.objects.get(pk=place_pk) for place_pk in places_pk]
    place_list = get_place_information(places)
    if len(place_list) > 0:
        for i in range(len(place_list)):
            place_list[i]["placeprice_min"] = float(place_list[i]["placeprice_min"])


        # =============================
        # Relevance (Feature)
        # =============================
        if option == 1:
            place_list_sorted = sorted(place_list, key=lambda k: k['feature'], reverse=True) 



        # =============================
        # Price
        # =============================
        elif option == 2 or option == 3:
            if option == 2: # Bigger Price
                place_list_sorted = sorted(place_list, key=lambda k: k['placeprice_min'], reverse=True) 
            elif option == 3: # Smaller Price
                place_list_sorted = sorted(place_list, key=lambda k: k['placeprice_min']) 


        # =============================
        # Rate
        # =============================
        elif option == 4:
            place_list_sorted = []
            pk_list = []

            # Here, we ignore "Nones"
            for i in range(len(place_list)):
                highest_rate = -1
                pk_selected = None
                for j in range(len(place_list)):
                    if place_list[j]["review_list"]["review_rates"] != "None":
                        rate_average = float(place_list[j]["review_list"]["review_rates"]["rate_average"])
                        if rate_average >= highest_rate:
                            if place_list[j]["pk"] not in pk_list:
                                pk_selected = place_list[j]["pk"]
                                highest_rate = rate_average

                if pk_selected is not None:
                    for j in range(len(place_list)):
                        if place_list[j]["pk"] == pk_selected:
                            place_list_sorted.append(place_list[j])
                            pk_list.append(place_list[j]["pk"])


            # We add the nones
            if len(place_list) != len(place_list_sorted):
                for i in range(len(place_list)):
                    if place_list[i]["review_list"]["review_rates"] == "None":
                        place_list_sorted.append(place_list[i])



        # =============================
        # Name
        # =============================
        elif option == 5 or option == 6:
            if option == 5: # A-Z
                place_list_sorted = sorted(place_list, key=lambda k: k['name'].upper()) 
            elif option == 6: # Z-A
                place_list_sorted = sorted(place_list, key=lambda k: k['name'].upper(), reverse=True) 

        # for i in range(len(place_list_sorted)):
        #     print(place_list_sorted[i])
        #     print()

        for i in range(len(place_list_sorted)):
            place_list_sorted[i]["placeprice_min"] = "%.2f"%place_list_sorted[i]["placeprice_min"]

        items_pk = []
        for i in range(len(place_list_sorted)):
            items_pk.append(place_list_sorted[i]["pk"])

        data = {"items_pk":items_pk }
    else:
        data = { "none": "True" }
    return data













def get_can_cancel(reservation, place):
    print()
    print()
    print()
    cancellation_policy = place.cancellation_policy
    print('cancellation_policy', cancellation_policy)

    days_before_event = (reservation.unavailability.day - datetime.today().date()).days
    print('days_before_event', days_before_event)

    hours_after_creating_reservation = (datetime.today().replace(tzinfo=None) - reservation.creation.replace(tzinfo=None)).total_seconds()/60/60
    print('hours_after_creating_reservation', hours_after_creating_reservation)

    place_reservation_price = reservation.value
    print('place_reservation_price', place_reservation_price)

    refund = False
    if cancellation_policy == "flexivel":
        # flexivel
        # Cancelamento até 48 horas após fazer a reserva e até 7 dias antes do evento, após este período pagamento integral do valor da reserva.
        if hours_after_creating_reservation < 48 and days_before_event > 7:
            refund = place_reservation_price
    elif cancellation_policy == "moderada":
        # moderada
        # Cancelamento até 48 horas após fazer a reserva e até 14 dias antes do evento, após este período pagamento integral do valor da reserva.
        if hours_after_creating_reservation < 48 and days_before_event > 14:
            refund = place_reservation_price
    elif cancellation_policy == "rigorosa":
        # rigorosa
        # 50% do reembolso caso o cancelamento ocorra ate 48 horas após fazer a reserva e até 21 dias antes do evento, após este período pagamento integral do valor da reserva.
        if hours_after_creating_reservation < 48 and days_before_event > 21:
            refund = place_reservation_price/2

    return [refund, days_before_event, hours_after_creating_reservation, place_reservation_price]










