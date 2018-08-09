import googlemaps
import math

from locacaoeventos.apps.place.placereservation.models import PlaceReservation, PlaceUnavailability
from locacaoeventos.apps.place.placereview.models import PlaceReview

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



def get_latlng_from_address_str(address_str):
    gmaps = googlemaps.Client(key ='AIzaSyCgsG2vhClFly8kadgTOHCX4wucOwgTiuw')
    geocode_result = gmaps.geocode(address_str)
    return [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]






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