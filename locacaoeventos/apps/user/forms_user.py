from django.forms import ModelForm, PasswordInput, fields
from django.core.mail import send_mail
from django import forms
import re
import datetime

from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile
from locacaoeventos.apps.user.sellerprofile.models import SellerProfile
from locacaoeventos.utils.forms import *

valida_cpf = True

class BuyerForm(TOCForm):
    photo = forms.FileField(required=False, widget=forms.FileInput, label="Foto de Perfil (opcional)")

    name = fields.CharField(required=True, label="Nome Completo")
    cpf_buyer = fields.CharField(required=False, label="CPF do responsável")
    email = fields.CharField(required=True, widget=forms.EmailInput, label="E-mail")

    day = fields.CharField(required=False, label="Data de Nascimento")
    month = fields.CharField(required=False, label="Data de Nascimento")
    year = fields.CharField(required=False, label="Data de Nascimento")
    cellphone = fields.CharField(required=False, label="Celular")
    gender = fields.CharField(required=False, label="Gênero")
    civil_status = fields.CharField(required=False, label="Status Civil")
    

    confirm = fields.CharField(required=True, widget=forms.PasswordInput,label="Senha", min_length="6")
    password = fields.CharField(required=False, widget=forms.PasswordInput,label="Senha", min_length="6")
    accepts_newsletter = forms.BooleanField(required=False, initial="checked")





    def __init__(self, *args, **kwargs):
        super(BuyerForm, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super(BuyerForm, self).clean()

        # Birthday
        day = str(cleaned_data.get('day'))
        month = str(cleaned_data.get('month'))
        year = str(cleaned_data.get('year'))
        if day != "" and month != "" and year != "":
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
            birthday = year + "-" + month + "-" + day
            try:
                datetime.datetime.strptime(birthday, '%Y-%m-%d')
            except:
                error_message = forms.ValidationError("ERROR")
                print("ERRO!1")
                self.add_error('day', error_message)

        # E-mail
        email = str(cleaned_data.get('email'))
        if BuyerProfile.objects.filter(email=email) or SellerProfile.objects.filter(email=email):
            error_message = forms.ValidationError("Já existe uma conta com este e-mail")
            self.add_error('email', error_message)


        # Photo
        photo = cleaned_data.get('photo')
        if photo:
            if not any(string in str(photo) for string in [".png", ".jpeg", ".jpg"]) and photo is not None:
                error_message = forms.ValidationError(
                    "Utilize um arquivo de imagem")
                self.add_error('photo', error_message)

        # CPF
        cpf = str(cleaned_data.get('cpf_buyer'))
        if cpf != "":
            if len(cpf) != 14:
                error_message = forms.ValidationError("CPF digitado incorretamente")
                self.add_error('cpf_buyer', error_message)
       
        cpf_num = re.sub('[^0-9]', '', cpf)
        if not validate_cpf(cpf_num) and valida_cpf:
            error_message = forms.ValidationError("CPF digitado incorretamente")
            print("ERRO!2/")
            self.add_error('cpf_buyer', error_message)

        cellphone = str(cleaned_data.get('cellphone'))
        print(cellphone)

        # Password
        password = str(cleaned_data.get('password'))
        confirm = str(cleaned_data.get('confirm'))
        if password != confirm:
            error_message = forms.ValidationError("Senhas diferentes!")
            self.add_error('password', error_message)





class FamilyMemberForm(TOCForm):
    name = fields.CharField(required=True, label="Nome do Familiar")
    gender = fields.CharField(required=True, label="Gênero")

    day = fields.CharField(required=True, label="Data de Nascimento")
    month = fields.CharField(required=True, label="Data de Nascimento")
    year = fields.CharField(required=True, label="Data de Nascimento")

    relation = fields.CharField(required=True, label="Grau de Parentesco")

    def __init__(self, *args, **kwargs):
        super(FamilyMemberForm, self).__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super(FamilyMemberForm, self).clean()

        # Birthday
        day = str(cleaned_data.get('day'))
        month = str(cleaned_data.get('month'))
        year = str(cleaned_data.get('year'))
        if day != "" and month != "" and year != "":
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day
            birthday = year + "-" + month + "-" + day
            try:
                datetime.datetime.strptime(birthday, '%Y-%m-%d')
            except:
                error_message = forms.ValidationError("Data inválida")
                self.add_error('day', error_message)

































class SellerForm(TOCForm):



    name_seller = fields.CharField(required=True, label="Nome do responsável")
    email_seller = fields.EmailField(required=True, widget=forms.EmailInput, label="E-mail")
    cellphone_seller = fields.CharField(required=True, label="Celular")


    cpf = fields.CharField(required=True, label="CPF do responsável")
    cnpj = fields.CharField(label="CNPJ do estabelecimento")

    password_seller = fields.CharField(required=False, widget=PasswordInput,label="Senha", min_length="6")
    confirm_seller = fields.CharField(required=False, widget=PasswordInput,label="Senha", min_length="6")

    accepts_newsletter_seller = forms.BooleanField(required=False, initial="checked", label="Aceita receber Newsletter")

    # PagarMe
    bank_code = fields.CharField(required=False, label="Código do Banco")
    agency = fields.CharField(required=False, label="Agência", max_length=5, min_length=5)
    account = fields.CharField(required=False, label="Conta Bancária", max_length=13, min_length=13)
    account_type = fields.CharField(required=False, label="Tipo de Conta")

    def clean(self):
        cleaned_data = super(SellerForm, self).clean()
        print(cleaned_data)
        
        # CPF
        cpf = str(cleaned_data.get('cpf'))
        if len(cpf) != 14:
            error_message = forms.ValidationError("CPF digitado incorretamente")
            self.add_error('cpf', error_message)
        cpf_num = re.sub('[^0-9]', '', cpf)
        if not validate_cpf(cpf_num):
            error_message = forms.ValidationError("CPF digitado incorretamente")
            self.add_error('cpf', error_message)

        # CNPJ
        cnpj = str(cleaned_data.get('cnpj'))
        if len(cnpj) != 18:
            error_message = forms.ValidationError("CNPJ digitado incorretamente")
            self.add_error('cnpj', error_message)

        cellphone = str(cleaned_data.get('cellphone_seller'))
        if len(cellphone) < 10:
            error_message = forms.ValidationError("Celular digitado incorretamente")
            self.add_error('cellphone_seller', error_message)

        # E-mail
        if "bank_code" not in cleaned_data:
            email_seller = str(cleaned_data.get('email_seller'))
            if BuyerProfile.objects.filter(email=email_seller) or SellerProfile.objects.filter(email=email_seller):
                error_message = forms.ValidationError("Já existe uma conta com este e-mail")
                self.add_error('email_seller', error_message)

        password_seller = str(cleaned_data.get('password_seller'))
        confirm_seller = str(cleaned_data.get('confirm_seller'))
        if password_seller is not None and confirm_seller is not None:
            if password_seller != confirm_seller:
                error_message = forms.ValidationError("Senhas diferentes!")
                self.add_error('password_seller', error_message)






def validate_cpf(cpf):
    if len(cpf) < 10:
        return False
    else:
        sum_tot = 0
        for i in range(1,10):
            sum_tot += int(cpf[i-1])*(11-i)
        dig1 = str((sum_tot*10)%11)
        if dig1 == '10':
            dig1 = '0'
        sum_tot = 0
        for i in range(1,11):
            sum_tot += int(cpf[i-1])*(12-i)
        dig2 = str((sum_tot*10)%11)
        if dig2 == '10':
            dig2 = '0'
        if dig1 == cpf[9] and dig2 == cpf[10]:
            return True
        else:
            return False