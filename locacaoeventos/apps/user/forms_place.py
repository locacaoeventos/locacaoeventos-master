from django.forms import fields
from django import forms
from django.contrib.postgres.forms import SimpleArrayField

import datetime

from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile
from locacaoeventos.utils.forms import *
from locacaoeventos.utils.place import *
from locacaoeventos.utils.general import *

class PlaceForm(TOCForm):

    name = fields.CharField(required=True, label="Nome")
    address = fields.CharField(required=True, label="Endereço")
    description = fields.CharField(required=True, widget=forms.Textarea, max_length=1024, label="Descrição")

    capacity = fields.CharField(required=True, widget=forms.NumberInput(), label="Capacidade")

    video = fields.CharField(
        required=False,
        label="Vídeo do Youtube (opcional)",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: www.youtube.com/watch?v=CoudYW6g'})
    )

    children_rides = forms.CharField(required=False, label="Brinquedos para Crianças")
    decoration = forms.CharField(required=False, label="Decorações")
    photos = SimpleArrayField(forms.CharField(required=True, label="Decorações"))
    menu = forms.FileField(required=False, widget=forms.FileInput)



    # Additional Informations
    alcoholic_drink = forms.BooleanField(required=False, label="Serve bebidas alcólicas")
    has_entertainment = forms.BooleanField(required=False, label="Enterteinimento")
    has_thematicdecoration = forms.BooleanField(required=False, label="Decoração Temática")
    has_childrenrides = forms.BooleanField(required=False, label="Brinquedo pra Crianças")
    has_costumes = forms.BooleanField(required=False, label="Fantasias para os Atores")
    has_parking = forms.BooleanField(required=False, label="Estacionamento")
    has_externalarea = forms.BooleanField(required=False, label="Área externa")
    has_music = forms.BooleanField(required=False, label="Música")
    has_illumination = forms.BooleanField(required=False, label="Iluminação")
    has_babychangingroom = forms.BooleanField(required=False, label="Fraldário")


    def __init__(self, *args, **kwargs):
        super(PlaceForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(PlaceForm, self).clean()
        address = cleaned_data.get('address')
        coordinates = get_latlng_from_address_str(address)
        try:
            coordinates = get_latlng_from_address_str(address)
        except:
            self.add_error('address', forms.ValidationError("Endereço inválido"))


        # Youtube Video
        video = cleaned_data.get('video')
        if video:
            if not any(string in video for string in ['youtube.com/watch?v=', 'youtube.com/embed/']) and video is not None:
                error_message = forms.ValidationError(
                    "Utilize um vídeo hospedado em youtube.com")
                self.add_error('video', error_message)

        # Menu file
        menu = cleaned_data.get('menu')
        if menu:
            if not any(string in str(menu) for string in [".png", ".jpeg", ".jpg", ".pdf"]) and menu is not None:
                error_message = forms.ValidationError(
                    "Utilize um arquivo de imagem ou pdf")
                self.add_error('menu', error_message)
