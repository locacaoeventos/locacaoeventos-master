from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse 

from django.contrib.auth.models import User

import datetime

from locacaoeventos.utils.main import *
from locacaoeventos.utils.feature import *
from .buyerprofile.models import BuyerProfile
from .sellerprofile.models import SellerProfile

from locacaoeventos.apps.place.placereservation.models import PlacePrice, PlaceUnavailability

# Celery
# from locacaoeventos.apps.user.tasks import test

class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        # context = base_context(request.user)
        # return render(request, "coming_soon.html", context)
        return render(request, "coming_soon.html")


class Blog(View):
    def get(self, request, *args, **kwargs):
        # context = base_context(request.user)

        
        # return render(request, "coming_soon.html", context)
        return HttpResponse("Blog")

class Email(View):
    def get(self, request, *args, **kwargs):
        return render(request, "emails/email_registration.html")


class Home(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        # now = datetime.datetime.now()
        # tomorrow = now + datetime.timedelta(seconds=10)

        # result = test.delay(2, 2)
        # result.ready()



        return render(request, "home.html", context)
    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        place = request.POST["place"]
        date = request.POST["date"]
        capacity = request.POST["capacity"]
        url_str = "/buffet/listar/?buffet=" + place + "&date=" + date + "&capacity=" + capacity



        return redirect(url_str)

class AboutUs(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["basemenu"] = "aboutus"
        return render(request, "about_us.html", context)

class Login(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        compra_buffet = request.GET.get("compra_buffet", None)
        context["basemenu"] = "login"
        if not request.user.is_authenticated:
            return render(request, "login.html", context)
        return redirect('/home')
    def post(self, request):
        context = base_context(request.user)
        context["basemenu"] = "login"
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username)
        if not user:
            username = username.lower()
            user = User.objects.filter(username=username)
            context = {
                'wrong_user': True
            }
            return render(request, "login.html", context)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if BuyerProfile.objects.filter(user=user):
                profile = BuyerProfile.objects.filter(user=user)[0]
            else:
                profile = SellerProfile.objects.filter(user=user)[0]
            if profile.is_active:
                login(request, user)
                if "next" in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return redirect('/home')
            else:
                context = {
                    'not_active': True
                }
                return render(request, "login.html", context)
        else:
            context = {
                'wrong_password': True
            }
            return render(request, "login.html", context)


class Logout(View):
    def get(self, request):
        context = base_context(request.user)
        if request.user.is_authenticated:
            auth.logout(request)
        return redirect('/home')


class TermsConditions(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "termsconditions.html", context)




class Teste(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        for placeprice in PlacePrice.objects.all():
            placeprice.description = '["aefawe fawef awef"]'
            placeprice.save()
        return render(request, "teste.html", context)




















class GoDaddyVerification(View):
    def get(self, request, *args, **kwargs):
        return render(request, "static/godaddy.html")



