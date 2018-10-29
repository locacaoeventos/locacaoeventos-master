import math

from datetime import datetime
import pytz

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
    return [
        {
            "name": "alcoholic_drink",
            "id_name": "id_alcoholic_drink",
            "label": "Serve bebidas alcólicas"
        },
        {
            "name": "has_entertainment",
            "id_name": "id_has_entertainment",
            "label": "Entretenimento"
        },
        {
            "name": "has_thematicdecoration",
            "id_name": "id_has_thematicdecoration",
            "label": "Decoração Temática"
        },
        {
            "name": "has_childrenrides",
            "id_name": "id_has_childrenrides",
            "label": "Brinquedo pra Crianças"
        },
        {
            "name": "has_costumes",
            "id_name": "id_has_costumes",
            "label": "Fantasias para os Atores"
        },
        {
            "name": "has_parking",
            "id_name": "id_has_parking",
            "label": "Estacionamento"
        },
        {
            "name": "has_externalarea",
            "id_name": "id_has_externalarea",
            "label": "Área externa"
        },
        {
            "name": "has_music",
            "id_name": "id_has_music",
            "label": "Música"
        },
        {
            "name": "has_illumination",
            "id_name": "id_has_illumination",
            "label": "Iluminação"
        },
        {
            "name": "has_babychangingroom",
            "id_name": "id_has_babychangingroom",
            "label": "Fraldário"
        },
    ]
























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











def get_place_information(places):
    place_list = []
    for place in places:
        place_dic = {
            "pk": place.pk,
            "name": place.name,
            "capacity": place.capacity,
            "address": place.address,
            "description": place.description,
            "lat": place.lat,
            "lng": place.lng,
        }
        photo = PlacePhoto.objects.filter(place=place)
        if photo:
            place_dic["photo"] = str(photo[0].photo.photo)

        placeprice_min = 9999999999999
        for placeprice in PlacePrice.objects.filter(place=place):
            if placeprice.value < placeprice_min:
                placeprice_min = placeprice.value
        if placeprice_min != 9999999999999:
            place_dic["placeprice_min"] = "%.2f"%placeprice_min
        # No objects allowed
        review_list = get_reviews_from_place(place)
        for i in range(len(review_list["review_list"])):
            review_list["review_list"][i]["buyerprofile"] = ""
        place_dic["review_list"] = review_list
        place_list.append(place_dic)
    return place_list














def filter_place_information(place_list_not_filtered, capacity, buffet, date):
    place_list = []
    if capacity == "" and buffet == "" and date == "":
        return place_list_not_filtered
    else:
        if buffet != "":
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

                if compare_strings(buffet, place["name"]):
                    if get_dic_by_key(place_list, "pk", place["pk"]) is None:
                        place_list.append(place)
        else:
            place_list = place_list_not_filtered


        # Filter by Capacity
        if capacity != "":
            place_list_filtered_capacity = []
            capacity_tolerance = 100
            capacity_analyse = int(capacity)
            for i in range(len(place_list)):
                place = place_list[i]
                if place["capacity"]+capacity_tolerance >= capacity_analyse and place["capacity"]-capacity_tolerance <= capacity_analyse:
                    place_list_filtered_capacity.append(place)


        # Filter by Date
        place_list_filtered_date = []
        if date != "":
            date_analyse_prep = date.replace(" ", "")
            date_analyse = datetime.strptime(date.replace(" ", "") + " 16", '%d/%m/%Y %H')

            for i in range(len(place_list)):
                place_obj = Place.objects.get(pk=place_list[i]["pk"])
                place_dic = place_list[i]
                unavailabilities = PlaceUnavailability.objects.filter(place=place_obj)
                is_occupied = False
                for unavailability in unavailabilities:
                    utc=pytz.UTC
                    if date_analyse.replace(tzinfo=utc) > unavailability.datetime_begin.replace(tzinfo=utc) and date_analyse.replace(tzinfo=utc) < unavailability.datetime_end.replace(tzinfo=utc):
                        is_occupied = True
                
                if not is_occupied:
                    place_list_filtered_date.append(place_dic)

        else:
            place_list_filtered_date = place_list_filtered_capacity

        return place_list_filtered_date
