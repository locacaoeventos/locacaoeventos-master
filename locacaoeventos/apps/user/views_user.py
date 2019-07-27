from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.template import loader

import datetime, random, string, os

from locacaoeventos.utils.main import *
from .views_general import Home
from django.contrib.auth.models import User

from .forms_user import *
from .buyerprofile.models import BuyerProfile, FamilyMember
from .sellerprofile.models import SellerProfile

from django.core.mail import send_mail


# Image from FB
import urllib, io
from PIL import Image


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
            str_body = ('Entrar nesse link para trocar sua senha ') + ' 123festas.com/usuario/trocar-senha/?user=' + str(profile.user.pk) + "&token=" + key
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













# ============================================================================================
# Create User
# ============================================================================================
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

            form_buyer = BuyerForm(request.POST, request.FILES, initial={"accepts_newsletter":True})
            context["form_buyer"] = form_buyer 
            context["form_seller"] = SellerForm()
            context["form_type"] = "buyer"
            if form_buyer.is_valid():
                user = User.objects.create(
                    username=form_buyer.cleaned_data["email"],
                    password="rawrawraw"
                )
                user.set_password(request.POST['password'])
                user.save()
                key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(23))

                # Birthday
                day = str(form_buyer.cleaned_data["day"])
                month = str(form_buyer.cleaned_data["month"])
                year = str(form_buyer.cleaned_data["year"])
                if day != "" and month != "" and year != "":
                    birthday = year + "-" + month + "-" + day
                else:
                    birthday = None

                buyer = BuyerProfile.objects.create(
                    user=user,
                    name=form_buyer.cleaned_data["name"],
                    cpf=form_buyer.cleaned_data["cpf_buyer"],
                    birthday=birthday,
                    cellphone=form_buyer.cleaned_data["cellphone"],
                    gender=form_buyer.cleaned_data["gender"],
                    civil_status=form_buyer.cleaned_data["civil_status"],
                    email=form_buyer.cleaned_data["email"],
                    key=key,
                    is_active=False,
                    accepts_newsletter=False
                )
                if "accepts_newsletter" in form_buyer.cleaned_data:
                    buyer.accepts_newsletter = True
                    buyer.save()
                str_subject = ('Confirmar cadastro no LOCACAO EVENTOS')
                user_pk = BuyerProfile.objects.get(email=form_buyer.cleaned_data["email"]).user.pk
                str_body = ('Obrigado pelo interesse no LOCACAO EVENTOS, por favor acesse esse site, para utilizar nossos serviços') + ' 123festas.com/usuario/confirmar-email/?user=' + str(user_pk) + "&token=" + key
                # send_mail(str_subject, str_body, 'christian.org96@gmail.com', [form_buyer.cleaned_data["email"]], fail_silently=False)
                # return redirect("/usuario/cadastro-concluido/")
            





                html_message = loader.render_to_string(
                    'emails/email_cliente_cadastro.html',
                    {
                        'user_name': form_buyer.cleaned_data["name"],
                        'token': key,
                        'user_pk': user_pk,
                        'is_seller': False

                    }
                )
                send_mail(str_subject,"",'christian.org96@gmail.com',[form_buyer.cleaned_data["email"]],fail_silently=True,html_message=html_message)

                return redirect("/usuario/cadastro-concluido/")



            else:
                return render(request, "user_create.html", context)
        elif "seller_form" in request.POST:
            form_seller = SellerForm(request.POST, initial={"accepts_newsletter_seller":True})
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
                    name=form_seller.cleaned_data["name_seller"],
                    email=form_seller.cleaned_data["email_seller"],
                    cpf=form_seller.cleaned_data["cpf"],
                    cnpj=form_seller.cleaned_data["cnpj"],
                    cellphone=form_seller.cleaned_data["cellphone_seller"],
                    accepts_newsletter=False,
                    key=key,
                    is_active=False
                )
                if "accepts_newsletter_seller" in form_seller.cleaned_data:
                    seller.accepts_newsletter = True
                    seller.save()


                user_pk = SellerProfile.objects.get(email=form_seller.cleaned_data["email_seller"]).user.pk
                str_subject = ('Confirmar cadastro no LOCACAO EVENTOS')
                str_body = ('Obrigado pelo interesse no LOCACAO EVENTOS, por favor acesse esse site, para utilizar nossos serviços') + ' 123festas.com/usuario/confirmar-email/?user=' + str(user_pk) + "&token=" + key + "&seller=true"
                # send_mail(str_titulo, str_body, 'christian.org96@gmail.com', [form_seller.cleaned_data["email_seller"]], fail_silently=False)


                html_message = loader.render_to_string(
                    'emails/email_cliente_cadastro.html',
                    {
                        'user_name': form_seller.cleaned_data["name_seller"],
                        'token': key,
                        'user_pk': user_pk,
                        'is_seller': True

                    }
                )
                send_mail(str_subject,"",'christian.org96@gmail.com',[form_seller.cleaned_data["email_seller"]],fail_silently=True,html_message=html_message)



                # DEBUG
                # seller = SellerProfile.objects.create(
                #     user=user,
                #     name=form_seller.cleaned_data["name_seller"],
                #     email=form_seller.cleaned_data["email_seller"],
                #     cpf=form_seller.cleaned_data["cpf"],
                #     cnpj=form_seller.cleaned_data["cnpj"],
                #     cellphone=form_seller.cleaned_data["cellphone_seller"],
                #     accepts_newsletter=False,
                #     key=key,
                #     is_active=True
                # )
                # if "accepts_newsletter_seller" in form_seller.cleaned_data:
                #     seller.accepts_newsletter = True
                #     seller.save()
                return redirect("/usuario/cadastro-concluido/")
            else:
                return render(request, "user_create.html", context)

class CreateUserCompleted(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "user_create_completed.html", context)





class CreateUserFacebook(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        fb_id = str(request.GET.get("id"))
        username = "FACEBOOKUSER" + fb_id

        user_list = User.objects.filter(username=username)
        if user_list:
            user = user_list[0]
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect("/home/")
        return render(request, "user_create_fb.html", context)
    def post(self, request, *args, **kwargs):
        context = {}
        fb_id = str(request.GET.get("id"))
        fb_name = str(request.GET.get("name").replace("%20", " "))
        fb_picture = str(request.GET.get("picture"))
        user_list = User.objects.filter(username="FACEBOOKUSER" + fb_id)
        user = User.objects.create(
            username="FACEBOOKUSER" + fb_id,
            password="rawrawraw"
        )
        user.set_password(fb_id+fb_id)
        user.save()
        email = request.POST["email"]

        if "accepts_newsletter" in request.POST:
            accepts_newsletter = True
        else:
            accepts_newsletter = False


        buyer = BuyerProfile.objects.create(
            user=user,
            name=fb_name,
            cpf=None,
            birthday=None,
            cellphone=None,
            gender=None,
            civil_status=None,
            email=email,
            key=fb_id,
            is_active=True,
            accepts_newsletter=False,
            photo="http://graph.facebook.com/" + fb_id + "/picture?type=normal"
        )


        user_pk = str(User.objects.get(username="FACEBOOKUSER"+fb_id).pk)
        return redirect("/usuario/confirmar-email/?key_FB=" + fb_id + "&user_pk=" + user_pk)








# ============================================================================================
# Confirm User
# ============================================================================================
class ConfirmEmail(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)

        # FB Create
        if "key_FB" in request.GET:
            key_FB = request.GET.get("key_FB")
            user_pk = request.GET.get("user_pk")
            user = User.objects.get(pk=user_pk)
            buyer = BuyerProfile.objects.get(user=user)
            if buyer.key == key_FB:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                context = base_context(request.user)
                context["token_valid"] = True
                context["create_family_member"] = True
                context["buyer_photo"] = buyer.photo
                context["buyer_name"] = buyer.name

                # Family Member
                context["familymember_list"] = FamilyMember.objects.filter(related_to=buyer)        
            else:
                context["token_valid"] = False
        # Normal Create

        else:
            user = User.objects.get(pk=request.GET["user"])
            if "seller" in request.GET:
                seller = SellerProfile.objects.get(user=user)
                token = request.GET["token"]
                if seller.key == token:
                    seller.is_active = True
                    seller.save()
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    context = base_context(request.user)
                    context["token_valid"] = True
                else:
                    context["token_valid"] = False
            else:
                buyer = BuyerProfile.objects.get(user=user)
                token = request.GET["token"]
                if buyer.key == token:
                    buyer.is_active = True
                    buyer.save()
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    context = base_context(request.user)
                    context["token_valid"] = True
                    context["create_family_member"] = True
                    context["buyer_photo"] = buyer.photo
                    context["buyer_name"] = buyer.name

                    # Family Member
                    context["familymember_list"] = FamilyMember.objects.filter(related_to=buyer)
                else:
                    context["token_valid"] = False
        return render(request, "user_create_token.html", context)















