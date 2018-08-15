import datetime, calendar, pytz

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from locacaoeventos.utils.main import base_context
from locacaoeventos.utils.datetime import translate_month
from locacaoeventos.apps.place.placecore.models import Place
from locacaoeventos.apps.place.placereservation.models import PlaceUnavailability




class CalendarExample(View):
    def get(self, request):
        return render(request, "calendar.html")


class CalendarAjax(View):
    def get(self, request):

        # Declaring Variables - Unavailability
        place = Place.objects.get(pk=request.GET.get("pk"))
        place_unavailability_list = []
        for unavailability in PlaceUnavailability.objects.filter(place=place):
            datetime_unavailability = unavailability.datetime_begin
            str_date_unavailability = str(datetime_unavailability.year) + "-" + str(datetime_unavailability.month) + "-" + str(datetime_unavailability.day)
            place_unavailability_list.append(str_date_unavailability)
            datetime_unavailability = unavailability.datetime_end
            str_date_unavailability = str(datetime_unavailability.year) + "-" + str(datetime_unavailability.month) + "-" + str(datetime_unavailability.day)
            place_unavailability_list.append(str_date_unavailability)


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
        list_month = ["<li>" + str(item+1) + "</li>" for item in range(calendar.monthrange(today_year,today_month)[1])]
        

        # Seting colors and markers
        for i in range(len(list_month)):
            day = i+1
            this_day = str(today_year) + "-" + str(today_month) + "-" + str(day)
            # We are in the current month
            if today_day:
                if day == today_day:
                    list_month[i] = "<li><span class='active'>" + str(i+1) + "</span></li>"
                elif day < today_day:
                    list_month[i] = "<li><span class='pass'>" + str(i+1) + "</span></li>"
                elif day > today_day and this_day in place_unavailability_list:
                    list_month[i] = "<li><span class='occupied' date_occupied='" + this_day + "'>" + str(i+1) + "</span></li>"
            
            else:
                # We are in a future month
                if today_year > today.year:
                    if this_day in place_unavailability_list:
                        list_month[i] = "<li><span class='occupied' date_occupied='" + this_day + "'>" + str(i+1) + "</span></li>"
                elif today_month > today.month and today_year >= today.year:
                    if this_day in place_unavailability_list:
                        list_month[i] = "<li><span class='occupied' date_occupied='" + this_day + "'>" + str(i+1) + "</span></li>"
                # We are in past month
                elif today_year < today.year:
                    list_month[i] = "<li><span class='pass'>" + str(i+1) + "</span></li>"
                elif today_month < today.month:
                    list_month[i] = "<li><span class='pass'>" + str(i+1) + "</span></li>"

        # Geting the first day of the month fiting with weekday
        weekday = datetime.datetime.strptime(str(today_year) + "-" + str(today_month) + "-1", "%Y-%m-%d").weekday()
        for i in range(weekday):
            list_month.insert(0, "<li></li>")

        data = {
            "today": today,
            "month": translate_month(calendar.month_name[today_month]),
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
        place = Place.objects.get(pk=pk)

        unavailability_this_day = []
        for unavailability in PlaceUnavailability.objects.filter(place=place):
            begin = unavailability.datetime_begin
            begin_str = begin.strftime("%Hh%M")
            end = unavailability.datetime_end
            end_str = end.strftime("%Hh%M")
            
            if begin.date() == datetime_this_day.date() or end.date() == datetime_this_day.date(): # Unavailability on this day
                if begin.date() < datetime_this_day.date() or end.date() > datetime_this_day.date(): # theres an exception
                    if begin.date() < datetime_this_day.date() and end.date() > datetime_this_day.date():
                        unavailability_this_day.append("00h00-23h59")

                    elif begin.date() < datetime_this_day.date():
                        unavailability_this_day.append("00h00-" + end_str)

                    elif end.date() > datetime_this_day.date():
                        unavailability_this_day.append(begin_str + "-23h59")

                else: # No exception
                    unavailability_this_day.append(begin_str + "-" + end_str)

        unavailability_this_day = sorted(unavailability_this_day)
        data["unavailability_this_day"] = unavailability_this_day
        this_day = datetime_this_day.strftime('%d')
        this_month = datetime_this_day.strftime('%B')
        this_year = datetime_this_day.strftime('%Y')
        data["this_day"] = this_day + " de " + translate_month(this_month) + " de " + this_year
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