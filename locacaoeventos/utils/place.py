import googlemaps

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
                    "buyerprofile": review.buyerprofile.name,
                    "creation": review.creation,
                    "comment": review.comment,
                    "rate_infraestructure": review.rate_infraestructure,
                    "rate_rides": review.rate_rides,
                    "rate_cost_benefit": review.rate_cost_benefit,
                    "rate_attendance": review.rate_attendance,
                    "rate_children_opinion": review.rate_children_opinion,
                    "rate": review.get_average_rate()
                })
                sum_rate_infraestructure += review.rate_infraestructure
                sum_rate_rides += review.rate_rides
                sum_rate_cost_benefit += review.rate_cost_benefit
                sum_rate_attendance += review.rate_attendance
                sum_rate_children_opinion += review.rate_children_opinion
                sum_rate_average += review.rate_infraestructure + review.rate_rides + review.rate_cost_benefit + review.rate_attendance + review.rate_children_opinion
                count_review += 1
    response["review_list"] = review_list
    response["review_rates"] = {
        "rate_infraestructure": sum_rate_infraestructure/count_review,
        "rate_rides": sum_rate_rides/count_review,
        "rate_cost_benefit": sum_rate_cost_benefit/count_review,
        "rate_attendance": sum_rate_attendance/count_review,
        "rate_children_opinion": sum_rate_children_opinion/count_review,
        "rate_average": sum_rate_average/count_review/5,
    }
    return response




def get_latlng_with_address_str(address_str):
    gmaps = googlemaps.Client(key ='AIzaSyCgsG2vhClFly8kadgTOHCX4wucOwgTiuw')
    geocode_result = gmaps.geocode(address_str)
    return [geocode_result[0]['geometry']['location']['lng'],geocode_result[0]['geometry']['location']['lat']]
