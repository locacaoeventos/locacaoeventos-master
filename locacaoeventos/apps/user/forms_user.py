from django.forms import ModelForm, PasswordInput, fields
from django.core.mail import send_mail
from django import forms

import datetime

from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile
from locacaoeventos.utils.forms import *

class BuyerForm(TOCForm):

    name = fields.CharField(required=True, label="Nome")
    email = fields.CharField(required=True, widget=forms.EmailInput, label="E-mail")
    password = fields.CharField(required=True, widget=PasswordInput,label="Senha", min_length="6")

    day = fields.CharField(required=True, label="Data de Nascimento")
    month = fields.CharField(required=True, label="Data de Nascimento")
    year = fields.CharField(required=True, label="Data de Nascimento")
    cellphone = fields.CharField(required=True, label="Celular")
    gender = fields.CharField(required=True, label="Gênero")
    civil_status = fields.CharField(required=True, label="Status Civil")
    
    photo = forms.FileField(required=False, widget=forms.FileInput, label="Foto de Perfil (opcional)")
    accepts_newsletter = forms.BooleanField(required=True, initial="checked")
    def __init__(self, *args, **kwargs):
        super(BuyerForm, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super(BuyerForm, self).clean()

        # Birthday
        day = str(cleaned_data.get('day'))
        month = str(cleaned_data.get('month'))
        year = str(cleaned_data.get('year'))
        if len(month) == 1:
            month = "0" + month
        if len(day) == 1:
            day = "0" + day
        birthday = year + "-" + month + "-" + day
        try:
            datetime.datetime.strptime(birthday, '%Y-%m-%d')
        except:
            error_message = forms.ValidationError("ERROR")
            self.add_error('day', error_message)

        # E-mail
        email = str(cleaned_data.get('email'))
        if BuyerProfile.objects.filter(email=email):
            error_message = forms.ValidationError("Já existe uma conta com este e-mail")
            self.add_error('email', error_message)


        # Photo
        photo = cleaned_data.get('photo')
        print(photo)
        if photo:
            if not any(string in str(photo) for string in [".png", ".jpeg", ".jpg"]) and photo is not None:
                error_message = forms.ValidationError(
                    "Utilize um arquivo de imagem")
                self.add_error('photo', error_message)





class SellerForm(TOCForm):
    email_seller = fields.EmailField(required=True, widget=forms.EmailInput, label="E-mail")
    password_seller = fields.CharField(required=True, widget=PasswordInput,label="Senha", min_length="6")
    cellphone_seller = fields.CharField(required=True, label="Celular")

    name_seller = fields.CharField(required=True, label="Nome do responsável")

    cpf = fields.CharField(required=True, label="CPF do responsável")
    cnpj = fields.CharField(label="CNPJ do estabelecimento")

    accepts_newsletter_seller = forms.BooleanField(required=True, initial="checked", label="Aceita receber Newsletter")
    def clean(self):
        cleaned_data = super(SellerForm, self).clean()

        # CPF
        cpf = str(cleaned_data.get('cpf'))
        if len(cpf) != 14:
            error_message = forms.ValidationError("CPF digitado incorretamente")
            self.add_error('cpf', error_message)


        # CNPJ
        cnpj = str(cleaned_data.get('cnpj'))
        if len(cnpj) != 18:
            error_message = forms.ValidationError("CNPJ digitado incorretamente")
            self.add_error('cnpj', error_message)



        # E-mail
        email_seller = str(cleaned_data.get('email_seller'))
        if BuyerProfile.objects.filter(email=email_seller):
            error_message = forms.ValidationError("Já existe uma conta com este e-mail")
            self.add_error('email_seller', error_message)

