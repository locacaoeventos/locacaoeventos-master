import datetime, calendar, locale

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from locacaoeventos.utils.forms import PhotoProvisoryForm
from locacaoeventos.utils.main import base_context
from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto, PhotoProvisory
from locacaoeventos.apps.place.placereservation.models import PlaceUnavailability
class UploadFile(View):
    def post(self, request):
        form = PhotoProvisoryForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            photo = form.save()
            data = {
                'is_valid': True,
                'name': photo.photo.name,
                'url': photo.photo.url,
                'pk': photo.pk
            }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class GetPhoto(View):
    def get(self, request):
        photos_list = request.GET.get("photos_list").split(",")
        photos = []
        for i in range(len(photos_list)):
            photo_provisory = PhotoProvisory.objects.get(pk=photos_list[i])
            photo = PlacePhoto.objects.get(photo=photo_provisory)
            photos.append({
                "url":str(photo.photo),
                "pk":str(photo.pk)
            })
        data = {"photos":photos}
        return JsonResponse(data)


class CalendarExample(View):
    def get(self, request):
        return render(request, "calendar.html")


class CalendarAjax(View):
    def get(self, request):
        try:
            locale.setlocale(locale.LC_ALL, 'pt.utf8')
        except:
            locale.setlocale(locale.LC_ALL, 'pt.UTF-8')

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
            "month": calendar.month_name[today_month],
            "year": today_year,
            "list_month": list_month,
        }
        return JsonResponse(data)



