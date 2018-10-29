import datetime
import pytz


from locacaoeventos.apps.place.placecore.models import Place, PlaceAdditionalInformation, PlaceFeature
from locacaoeventos.apps.place.placereservation.models import PlaceReservation
from locacaoeventos.apps.place.placereview.models import PlaceReview



def update_feature_places():
    e=2.71828
    now = datetime.datetime.now()
    utc = pytz.UTC
    placefeature = PlaceFeature.objects.all()[0]
    for place in Place.objects.filter(is_active=True, has_finished_basic=True):
        data_criacao = place.creation

        # data_criacao
        qtdade_infoadicional = 0
        for attr, value in PlaceAdditionalInformation.objects.get(place=place).__dict__.items():
            if value == True:
                qtdade_infoadicional += 1

        # reservation
        reservation_value = 0
        for placereservation in PlaceReservation.objects.filter(place=place):
            placereview = PlaceReview.objects.filter(reservation=placereservation)
            if placereview:
                placereview = placereview[0]
                placereview_average = (placereview.rate_infraestructure + placereview.rate_rides + placereview.rate_cost_benefit + placereview.rate_attendance + placereview.rate_children_opinion)/5

                delta_time = (now.replace(tzinfo=utc)-placereview.creation.replace(tzinfo=utc)).days
                
                if delta_time <= 1:
                    reservation_value += placefeature.reservation_factor_firstday*placereview_average
                else:
                    print(placereview_average)
                    print(placereview_average)
                    print(placereview_average)
                    reservation_value += 1/(e**(float(placereview_average)*float(placefeature.reservation_factor)))
        print(reservation_value)

    return "check"