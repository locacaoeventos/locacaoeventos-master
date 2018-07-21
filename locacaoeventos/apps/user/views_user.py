from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import auth

import datetime
import random
import string

from locacaoeventos.utils.main import *
from django.contrib.auth.models import User

from .forms_user import *
from .buyerprofile.models import BuyerProfile
from .sellerprofile.models import SellerProfile

from django.core.mail import send_mail


class Home(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "home.html", context)
    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        place = request.POST["place"]
        date = request.POST["date"]
        capacity = request.POST["capacity"]
        url_str = "/buffet/listar/?place=" + place + "&date=" + date + "&capacity=" + capacity

        return redirect(url_str)


class ComingSoon(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "coming_soon.html", context)



class AboutUs(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["basemenu"] = "aboutus"
        return render(request, "about_us.html", context)






class Login(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        context["basemenu"] = "login"
        if not request.user.is_authenticated:
            return render(request, "login.html", context)
        return redirect('/')
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
                return redirect('/')
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
        return redirect('/')



class TermsConditions(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "termsconditions.html", context)

class CreateUser(View):
    def get(self, request, *args, **kwargs):
        context = {
            "form_buyer": BuyerForm(), 
            "form_seller": SellerForm(),
        }
        context["basemenu"] = "register"
        return render(request, "user_create.html", context)
    def post(self, request, *args, **kwargs):
        context = {}
        context["basemenu"] = "register"

        if "buyer_form" in request.POST:
            form_buyer = BuyerForm(request.POST)
            context["form_buyer"] = form_buyer 
            context["form_seller"] = SellerForm()
            context["form_type"] = "buyer"

            if form_buyer.is_valid():
                
                # Birthday
                day = str(form_buyer.cleaned_data["day"])
                month = str(form_buyer.cleaned_data["month"])
                year = str(form_buyer.cleaned_data["year"])
                birthday = year + "-" + month + "-" + day

                user = User.objects.create(
                    username=form_buyer.cleaned_data["email"],
                    password="rawrawraw"
                )

                user.set_password(request.POST['password'])
                user.save()
                key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(23))
                buyer = BuyerProfile.objects.create(
                    user=user,
                    name=form_buyer.cleaned_data["name"],
                    birthday=birthday,
                    cellphone=form_buyer.cleaned_data["cellphone"],
                    gender=form_buyer.cleaned_data["gender"],
                    civil_status=form_buyer.cleaned_data["civil_status"],
                    email=form_buyer.cleaned_data["email"],
                    key=key,
                    is_active=False
                )
                str_titulo = ('Confirmar cadastro no LOCACAO EVENTOS')
                str_body = ('Obrigado pelo interesse no LOCACAO EVENTOS, por favor acesse esse site, para utilizar nossos serviços') + ' localhost:8000/usuario/confirmar-email-comprador/?user=' + str(user.pk) + "&token=" + key
                send_mail(str_titulo, str_body, 'christian.org96@gmail.com', [form_buyer.cleaned_data["email"]], fail_silently=False)
                return redirect("/usuario/cadastro-concluido/")
            else:
                return render(request, "user_create.html", context)



        elif "seller_form" in request.POST:
            form_seller = SellerForm(request.POST)
            context["form_buyer"] = BuyerForm()
            context["form_seller"] = form_seller
            context["form_type"] = "seller"
            if form_seller.is_valid():
                user = User.objects.create(
                    username=form_seller.cleaned_data["email_seller"],
                    password="rawrawraw"
                )

                user.set_password(request.POST['password_seller'])
                user.save()
                key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(23))
                seller = SellerProfile.objects.create(
                    user=user,
                    name=form_seller.cleaned_data["name"],
                    email=form_seller.cleaned_data["email_seller"],
                    cpf=form_seller.cleaned_data["cpf"],
                    cnpj=form_seller.cleaned_data["cnpj"],
                    key=key,
                    is_active=False
                )
                str_titulo = ('Confirmar cadastro no LOCACAO EVENTOS')
                str_body = ('Obrigado pelo interesse no LOCACAO EVENTOS, por favor acesse esse site, para utilizar nossos serviços') + ' localhost:8000/usuario/confirmar-email-comprador/?user=' + str(user.pk) + "&token=" + key + "&seller=true"
                send_mail(str_titulo, str_body, 'christian.org96@gmail.com', [form_seller.cleaned_data["email"]], fail_silently=False)
                return redirect("/usuario/cadastro-concluido/")
            else:
                return render(request, "user_create.html", context)


class CreateUserCompleted(View):
    def get(self, request, *args, **kwargs):
        context = {"form": BuyerForm()}
        return render(request, "user_create_completed.html", context)


class ConfirmEmailBuyer(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        user = User.objects.get(pk=request.GET["user"])
        if "seller" in request.GET:
            seller = SellerProfile.objects.get(user=user)
            token = request.GET["token"]
            if seller.key == token:
                context["token_valid"] = True
                seller.is_active = True
                seller.save()
            else:
                context["token_valid"] = False

        else:
            buyer = BuyerProfile.objects.get(user=user)
            token = request.GET["token"]
            if buyer.key == token:
                context["token_valid"] = True
                buyer.is_active = True
                buyer.save()
            else:
                context["token_valid"] = False
        return render(request, "user_create_token.html", context)




class ForgotPassword(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "forgot_password.html", context)
    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        email = request.POST["email"]
        buyers = BuyerProfile.objects.filter(email=email)
        sellers = SellerProfile.objects.filter(email=email)
        if buyers or sellers:
            if buyers:
                profile = buyers[0]
            else:
                profile = sellers[0]
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(23))
            profile.key = key
            profile.save()
            str_titulo = ('Nova senha no LOCACAO EVENTOS')
            str_body = ('Entrar nesse link para trocar sua senha ') + ' localhost:8000/usuario/trocar-senha/?user=' + str(profile.user.pk) + "&token=" + key
            send_mail(str_titulo, str_body, 'christian.org96@gmail.com', [request.POST["email"]], fail_silently=False)
            return render(request, "forgot_password_completed.html", context)

        else:
            context["email_doesntexist"] = True
            return render(request, "forgot_password.html", context)



class ChangePassword(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        user = User.objects.get(pk=request.GET["user"])
        buyers = BuyerProfile.objects.filter(user=user)
        sellers = SellerProfile.objects.filter(user=user)
        if buyers:
            profile = buyers[0]
        else:
            profile = sellers[0]
        token = request.GET["token"]
        if profile.key == token:
            context["token_valid"] = True
            profile.is_active = True
            profile.save()
        else:
            context["token_valid"] = False
        return render(request, "forgot_password_change.html", context)

    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        user = User.objects.get(pk=request.GET["user"])

        password = request.POST["password"]
        user.set_password(password)
        user.save()

        return redirect("/login")

















class Teste(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "teste.html", context)

