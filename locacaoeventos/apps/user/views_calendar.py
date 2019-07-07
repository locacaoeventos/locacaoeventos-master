import datetime, calendar, pytz, ast

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from locacaoeventos.utils.main import base_context
from locacaoeventos.utils.datetime import translate_month, next_days
from locacaoeventos.utils.general import remove_left_zero

from locacaoeventos.apps.place.placecore.models import Place
from locacaoeventos.apps.place.placereservation.models import PlaceUnavailability, PlaceSazonality




class CalendarExample(View):
    def get(self, request):
        return render(request, "calendar.html")


def get_unavailabilities(place, period):
    if period != "none" and period != None:
        period = ast.literal_eval(period)
        placeunavailabilities = []




            


        # Filtering period of unavailability (selected on place detail)
        if period[0] == 1:
            placeunavailabilities += PlaceUnavailability.objects.filter(place=place, period="min")
        
        # Filtering period of unavailability (selected on place detail)
        if period[1] == 1:
            placeunavailabilities += PlaceUnavailability.objects.filter(place=place, period="max")


        # Treating data
        place_unavailability_list_with_period = []
        place_unavailability_list = []
        for unavailability in placeunavailabilities:
            day = unavailability.day
            str_date_unavailability = str(day.year) + "-" + str(day.month) + "-" + str(day.day)
            date_unavailability = datetime.datetime.strptime(str_date_unavailability, '%Y-%m-%d')
            place_unavailability_list.append(str_date_unavailability)
            place_unavailability_list_with_period.append([str_date_unavailability, unavailability.period])

            unavailability_next_days = next_days(365, date_unavailability)

            if unavailability.repeat == "week":
                # 0 = Monday
                for i in range(len(unavailability_next_days)):
                    next_day = unavailability_next_days[i]
                    if unavailability.day.weekday() == next_day.weekday():
                        str_date_unavailability = str(next_day.year) + "-" + str(next_day.month) + "-" + str(next_day.day)
                        place_unavailability_list.append(str_date_unavailability)
                        place_unavailability_list_with_period.append([str_date_unavailability, unavailability.period])

            if unavailability.repeat == "biweek":
                # Algorithm from week, but for biweeek
                for i in range(len(unavailability_next_days)):
                    if i%2 == 0:
                        next_day = unavailability_next_days[i]
                        if unavailability.day.weekday() == next_day.weekday():
                            str_date_unavailability = str(next_day.year) + "-" + str(next_day.month) + "-" + str(next_day.day)
                        place_unavailability_list.append(str_date_unavailability)
                        place_unavailability_list_with_period.append([str_date_unavailability, unavailability.period])

            if unavailability.repeat == "month":
                for i in range(len(unavailability_next_days)):
                    next_day = unavailability_next_days[i]
                    if unavailability.day.day == next_day.day:
                        str_date_unavailability = str(next_day.year) + "-" + str(next_day.month) + "-" + str(next_day.day)
                        place_unavailability_list.append(str_date_unavailability)
                        place_unavailability_list_with_period.append([str_date_unavailability, unavailability.period])
    else:
        place_unavailability_list = []
        place_unavailability_list_with_period = []
    return place_unavailability_list, place_unavailability_list_with_period





















def get_str_occupied(this_day, place_unavailability_list_with_period):
    index = []
    for i in range(len(place_unavailability_list_with_period)):
        if this_day == place_unavailability_list_with_period[i][0]:
            index.append(i) 

    period = [0,0]
    for i in range(len(index)):
        if place_unavailability_list_with_period[index[i]][1] == "min":
            period[0] = 1
        elif place_unavailability_list_with_period[index[i]][1] == "max":
            period[1] = 1

    str_occupied = ""
    if period == [1,0]:
        str_occupied = "occupied_min"
    elif period == [0,1]:
        str_occupied = "occupied_max"

    elif period == [1,1]:
        str_occupied = "occupied"
    
    return str_occupied

class CalendarAjax(View):
    def get(self, request):
        place = Place.objects.get(pk=request.GET.get("pk"))

        # Unavailability
        period = request.GET.get("period")
        if period == None:
            period = "[1,1]"
        place_unavailability_list, place_unavailability_list_with_period = get_unavailabilities(place, period)
        # Today, this month, this year
        today = datetime.datetime.today()
        today_month = request.GET.get("meses", None) # Checking if it's changing month
        if today_month == None:
            today_month = str(0)
        if today_month == str(0):
            today_day = int(today.day)
            today_month = int(today.month)
            today_year = int(today.year)
        else:
            today_day = None
            today_month = int(today.month) + int(today_month)
            if today_month > 12:
                today_month -= 12
                today_year = int(today.year) + 1
            else:
                today_year = int(today.year)
            

        # Correct size of month
        count_day = calendar.monthrange(today_year, today_month)
        list_month = ["<li class='day_select calendar_class_day'><span class='day_option'>" + str(item+1) + "</span></li>" for item in range(calendar.monthrange(today_year,today_month)[1])]
        

        # Seting colors and markers
        for i in range(len(list_month)):
            day = i+1
            this_day = str(today_year) + "-" + str(today_month) + "-" + str(day)
            # We are in the current month
            if today_day:
                if day == today_day:
                    list_month[i] = "<li class='calendar_class_day'><span class='day_option day_colored active day_select'>" + str(i+1) + "</span></li>"
                elif day < today_day:
                    list_month[i] = "<li class='calendar_class_day'><span class='day_option day_colored pass'>" + str(i+1) + "</span></li>"
                elif day > today_day and this_day in place_unavailability_list:
                    str_occupied = get_str_occupied(this_day, place_unavailability_list_with_period)
                    list_month[i] = "<li class='calendar_class_day'><span class='day_option day_colored " + str_occupied + "' date_occupied='" + this_day + "'>" + str(i+1) + "</span></li>"
            
            else:
                # We are in a future month
                if today_year > today.year:
                    if this_day in place_unavailability_list:
                        str_occupied = get_str_occupied(this_day, place_unavailability_list_with_period)
                        list_month[i] = "<li class='calendar_class_day'><span class='day_option day_colored " + str_occupied + "' date_occupied='" + this_day + "'>" + str(i+1) + "</span></li>"
                elif today_month > today.month and today_year >= today.year:
                    if this_day in place_unavailability_list:
                        str_occupied = get_str_occupied(this_day, place_unavailability_list_with_period)
                        list_month[i] = "<li class='calendar_class_day'><span class='day_option day_colored " + str_occupied + "' date_occupied='" + this_day + "'>" + str(i+1) + "</span></li>"
                # We are in past month
                elif today_year < today.year:
                    list_month[i] = "<li class='calendar_class_day'><span class='day_option day_colored pass'>" + str(i+1) + "</span></li>"
                elif today_month < today.month:
                    list_month[i] = "<li class='calendar_class_day'><span class='day_option day_colored pass'>" + str(i+1) + "</span></li>"

        # Geting the first day of the month fiting with weekday
        weekday = datetime.datetime.strptime(str(today_year) + "-" + str(today_month) + "-1", "%Y-%m-%d").weekday()
        for i in range(weekday):
            list_month.insert(0, "<li class='calendar_class_day'></li>")

        data = {
            "today": today,
            "month": translate_month(calendar.month_name[today_month]),
            "month_int": today_month,
            "year": today_year,
            "list_month": list_month,
        }
        return JsonResponse(data)


class UnavailabilityDetailAjax(View):
    def get(self, request, *args, **kwargs):
        utc = pytz.UTC
        data = {}

        pk = request.GET.get("pk")
        this_day = request.GET.get("this_day")
        datetime_this_day = datetime.datetime.strptime(this_day, '%Y-%m-%d').replace(tzinfo=utc)
        this_day = datetime_this_day.strftime('%d')
        this_month = datetime_this_day.strftime('%m')
        this_year = datetime_this_day.strftime('%Y')
        this_day_yyyy_mm_dd = this_year + "-" + remove_left_zero(this_month) + "-" + remove_left_zero(this_day)

        place = Place.objects.get(pk=pk)

        unavailability_this_day = []
        place_unavailability_list_min = get_unavailabilities(place, "[1,0]")
        place_unavailability_list_max = get_unavailabilities(place, "[0,1]")
        unavailability_this_day = []
        for unavailability in place_unavailability_list_min:
            if unavailability == this_day_yyyy_mm_dd:
                unavailability_this_day.append(str(place.period_soon_begin.strftime("%H:%M")) + "-" + str(place.period_soon_end.strftime("%H:%M")))
                break
        for unavailability in place_unavailability_list_max:
            if unavailability == this_day_yyyy_mm_dd:
                unavailability_this_day.append(str(place.period_late_begin.strftime("%H:%M")) + "-" + str(place.period_late_end.strftime("%H:%M")))
                break

        unavailability_this_day = sorted(unavailability_this_day)
        data["unavailability_this_day"] = unavailability_this_day

        this_month_eng = datetime_this_day.strftime('%B')
        data["this_day"] = this_day + " de " + translate_month(this_month_eng) + " de " + this_year
        return JsonResponse(data)





























class CalendarSeasonAjax(View):
    def get(self, request):


        # Declaring Variables - Others
        today = datetime.datetime.today()
        today_month = request.GET.get("meses", None) # Checking if it's changing month
        if today_month == None:
            today_month = str(0)
        if today_month == str(0):
            today_day = int(today.day)
            today_month = int(today.month)
            today_year = int(today.year)
        else:
            today_day = None
            today_month = int(today.month) + int(today_month)
            if today_month > 12:
                today_month -= 12
                today_year = int(today.year) + 1
            else:
                today_year = int(today.year)
        # Correct size of month
        count_day = calendar.monthrange(today_year, today_month)
        list_month = ["<li class='calendar_class_day_season'>" + str(item+1) + "</li>" for item in range(calendar.monthrange(today_year,today_month)[1])]
        

        # Seting colors and markers
        for i in range(len(list_month)):
            day = i+1
            this_day = str(today_year) + "-" + str(today_month) + "-" + str(day)
            # We are in the current month
            if today_day:
                if day == today_day:
                    list_month[i] = "<li class='calendar_class_day_season'><span class='active'>" + str(i+1) + "</span></li>"
                elif day < today_day:
                    list_month[i] = "<li class='calendar_class_day_season'><span class='pass'>" + str(i+1) + "</span></li>"
            else:
                # We are in past month
                if today_year < today.year:
                    list_month[i] = "<li class='calendar_class_day_season'><span class='pass'>" + str(i+1) + "</span></li>"
                elif today_month < today.month:
                    list_month[i] = "<li class='calendar_class_day_season'><span class='pass'>" + str(i+1) + "</span></li>"

        # Geting the first day of the month fiting with weekday
        weekday = datetime.datetime.strptime(str(today_year) + "-" + str(today_month) + "-1", "%Y-%m-%d").weekday()
        for i in range(weekday):
            list_month.insert(0, "<li class='calendar_class_day_season'></li>")

        data = {
            "today": today,
            "month": translate_month(calendar.month_name[today_month]),
            "month_int": today_month,
            "year": today_year,
            "list_month": list_month,

        }
        return JsonResponse(data)






























































class CalendarInputAjax(View):
    def get(self, request):

        # Declaring Variables - Others
        today = datetime.datetime.today()
        today_month = request.GET.get("meses", None) # Checking if it's changing month
        if today_month == None:
            today_month = str(0)
        if today_month == str(0):
            today_day = int(today.day)
            today_month = int(today.month)
            today_year = int(today.year)
        else:
            today_day = None
            today_month = int(today.month) + int(today_month)
            if today_month > 12:
                today_month -= 12
                today_year = int(today.year) + 1
            else:
                today_year = int(today.year)
            

        # Correct size of month
        count_day = calendar.monthrange(today_year, today_month)
        list_month = ["<li class='calendar_class_day'>" + str(item+1) + "</li>" for item in range(calendar.monthrange(today_year,today_month)[1])]
        
        # Seting colors and markers
        for i in range(len(list_month)):
            day = i+1
            this_day = str(today_year) + "-" + str(today_month) + "-" + str(day)
            # We are in the current month
            if today_day:
                if day == today_day:
                    list_month[i] = "<li class='calendar_class_day'><span class='active'>" + str(i+1) + "</span></li>"
                elif day < today_day:
                    list_month[i] = "<li class='calendar_class_day'><span class='pass'>" + str(i+1) + "</span></li>"
            else:
                # We are in past month
                if today_year < today.year:
                    list_month[i] = "<li class='calendar_class_day'><span class='pass'>" + str(i+1) + "</span></li>"
                elif today_month < today.month:
                    list_month[i] = "<li class='calendar_class_day'><span class='pass'>" + str(i+1) + "</span></li>"

        # Geting the first day of the month fiting with weekday
        weekday = datetime.datetime.strptime(str(today_year) + "-" + str(today_month) + "-1", "%Y-%m-%d").weekday()
        for i in range(weekday):
            list_month.insert(0, "<li class='calendar_class_day'></li>")

        data = {
            "today": today,
            "month": translate_month(calendar.month_name[today_month]),
            "month_int": today_month,
            "year": today_year,
            "list_month": list_month,

        }
        return JsonResponse(data)