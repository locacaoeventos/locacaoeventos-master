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
            place_list = place_list_not_filtered



        # Filter by Capacity
        if capacity != "" and capacity != "sem":
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
            place_list_filtered_capacity = place_list

        # Filter by Date
        place_list_filtered_date = []
        if date != "":
            date_analyse_prep = date.replace(" ", "")
            date_analyse = datetime.strptime(date.replace(" ", "") + " 0", '%d/%m/%Y %H')
            day = date_analyse.day
            month = date_analyse.month
            year = date_analyse.year
            print(day)
            print(month)
            print(year)
            for i in range(len(place_list)):
                place_obj = Place.objects.get(pk=place_list[i]["pk"])
                place_dic = place_list[i]
                unavailabilities = PlaceUnavailability.objects.filter(place=place_obj)
                is_occupied = False
                for unavailability in unavailabilities:
                    if date_analyse.replace(tzinfo=pytz.UTC) == unavailability.day:
                        is_occupied = True
                    # if date_analyse.replace(tzinfo=utc) > unavailability.datetime_begin.replace(tzinfo=utc) and date_analyse.replace(tzinfo=utc) < unavailability.datetime_end.replace(tzinfo=utc):
                    #     is_occupied = True
                
                if not is_occupied:
                    place_list_filtered_date.append(place_dic)

        else:
            place_list_filtered_date = place_list_filtered_capacity

        return place_list_filtered_date



def get_placeprices(place):
    placeprices = []
    for placeprice in PlacePrice.objects.filter(place=place):
        placeprices.append({
            "value": placeprice.value,
            "name": placeprice.name,
            "description": ast.literal_eval(placeprice.description),
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
                place_list_sorted = sorted(place_list, key=lambda k: k['name']) 
            elif option == 6: # Z-A
                place_list_sorted = sorted(place_list, key=lambda k: k['name'], reverse=True) 

        for i in range(len(place_list_sorted)):
                print(place_list_sorted[i])

        for i in range(len(place_list_sorted)):
            place_list_sorted[i]["placeprice_min"] = "%.2f"%place_list_sorted[i]["placeprice_min"]

        items_pk = []
        for i in range(len(place_list_sorted)):
            items_pk.append(place_list_sorted[i]["pk"])

        data = {"items_pk":items_pk }
    else:
        data = { "none": "True" }
    return data