import pytz

from locacaoeventos.utils.place import *

from locacaoeventos.apps.place.placecore.models import Place, PlaceAdditionalInformation, PlaceFeature, PlaceVisualization
from locacaoeventos.apps.place.placereservation.models import PlaceReservation
from locacaoeventos.apps.place.placereview.models import PlaceReview



def update_feature_places():
    e=2.71828
    now = datetime.now()
    utc = pytz.UTC
    placefeature = PlaceFeature.objects.all()[0]
    place_list = []
    for place in Place.objects.filter(is_active=True, has_finished_basic=True):
        place_dic = get_single_place_dic(place)


        print(" ===================== BEGIN PLACE =====================")
        data_criacao = place.creation

        # Visuaization
        visualization_value = 0
        visualization_factor_firstday = placefeature.visualization_factor_firstday
        visualization_factor = placefeature.visualization_factor
        place_visualization_list = []
        for placevisualization in PlaceVisualization.objects.filter(place=place):
            print("----- BEGIN VISUALIZATION -----")
            delta_time = (now.replace(tzinfo=utc)-placevisualization.creation.replace(tzinfo=utc)).days
            # First-day-Factor for Revisualization
            if delta_time <= 1:
                value = visualization_factor_firstday
                print("firstday")
            else:
                value = 1*(1/(e**(delta_time*visualization_factor)))
                print(delta_time)
            visualization_value += value
            print(value)
            print("----- END VISUALIZATION -----")
            place_visualization_list.append({
                "delta_time": delta_time,
                "value": value,
            })
        place_dic["visualization_list"] = place_visualization_list
        place_dic["visualization_value"] = visualization_value

        print(visualization_value)
        print(" ====== END VIEW =====")



        # Review
        review_value = 0
        review_factor_firstday = placefeature.review_factor_firstday
        review_factor = placefeature.review_factor



        for i in range(len(place_dic["review_list"]["review_list"])):
            print("----- BEGIN REVIEW -----")
            placereview_dic = place_dic["review_list"]["review_list"][i]
            placereview = PlaceReview.objects.get(pk=placereview_dic["pk"])
            placereview_average = (placereview_dic["rate_infraestructure"] + placereview_dic["rate_rides"] + placereview_dic["rate_cost_benefit"] + placereview_dic["rate_attendance"] + placereview_dic["rate_children_opinion"])/5
            print(placereview_average)

            delta_time = (now.replace(tzinfo=utc)-placereview.creation.replace(tzinfo=utc)).days
            
            # First-day-Factor for Review
            if delta_time <= 1:
                value = review_factor_firstday*placereview_average
                print("firstday")
            else:
                value = placereview_average*1/(e**(delta_time*review_factor))
                print(delta_time)
            print(value)
            place_dic["review_list"]["review_list"][i]["delta_time"] = delta_time
            place_dic["review_list"]["review_list"][i]["value"] = value
            review_value += value
            print("----- END REVIEW -----")
        place_dic["review_list"]["review_value"] = review_value
        print(review_value)

        print("=========================")
        print(place_dic)
        print(" ===================== END PLACE =====================")
        place_list.append(place_dic)
    return place_list