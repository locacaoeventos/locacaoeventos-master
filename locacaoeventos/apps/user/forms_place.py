from django.forms import fields
from django import forms
from django.contrib.postgres.forms import SimpleArrayField

import datetime

from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile
from locacaoeventos.utils.forms import *

class PlaceForm(TOCForm):

    name = fields.CharField(required=True, label="Nome")
    address = fields.CharField(required=True, label="Endereço")
    description = fields.CharField(required=True, widget=forms.Textarea, label="Descrição")

    capacity = fields.CharField(required=True, widget=forms.NumberInput, label="Capacidade")
    size = fields.CharField(required=True, widget=forms.NumberInput, label="Tamanho")

    video = fields.CharField(
        required=False,
        label="Vídeo do Youtube (opcional)",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: www.youtube.com/watch?v=CoudYW6g'})
    )

    children_rides = SimpleArrayField(forms.CharField(required=False, label="Brinquedos para Crianças"))
    decoration = SimpleArrayField(forms.CharField(required=False, label="Decorações"))
    photos = SimpleArrayField(forms.CharField(required=True, label="Decorações"))
    menu = forms.FileField(required=True)


    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PlaceForm, self).clean()

        # Birthday
        # day = str(cleaned_data.get('day'))
        # month = str(cleaned_data.get('month'))
        # year = str(cleaned_data.get('year'))
        # if len(month) == 1:
        #     month = "0" + month
        # if len(day) == 1:
        #     day = "0" + day
        # birthday = year + "-" + month + "-" + day
        # try:
        #     datetime.datetime.strptime(birthday, '%Y-%m-%d')
        # except:
        #     error_message = forms.ValidationError("ERROR")
        #     self.add_error('day', error_message)

        # # E-mail
        # email = str(cleaned_data.get('email'))
        # if BuyerProfile.objects.filter(email=email):
        #     error_message = forms.ValidationError("Já existe uma conta com este e-mail")
        #     self.add_error('email', error_message)

