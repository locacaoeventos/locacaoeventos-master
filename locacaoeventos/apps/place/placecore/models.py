from django.db import models

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from PIL import Image

from locacaoeventos.apps.user.sellerprofile.models import SellerProfile

class Place(models.Model):
    # Default
    creation = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    relevance = models.FloatField("Relevância", default=0)
    visualization = models.IntegerField("Visualizações", default=0)

    is_authorized_by_admin = models.BooleanField(default=False)
    has_finished_basic = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Place Form
    name = models.CharField("Nome", max_length=64)
    address = models.CharField("Endereço", max_length=256)
    description = models.CharField("Descrição", max_length=512)

    capacity = models.IntegerField("Capacidade")
    size = models.FloatField("Tamanho")
    video = models.CharField("Video URL", max_length=128, blank=True)
    children_rides = ArrayField(models.CharField(max_length=200), blank=True)
    decoration = ArrayField(models.CharField(max_length=200), blank=True)

    menu = models.FileField('Menu', upload_to='place/menu', blank=True)
    # Auto-Fill
    sellerprofile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name="SellerProfile")
    lat = models.FloatField("Latitude")
    lng = models.FloatField("Longitude")


    def __str__(self):
        return self.name




class PlaceAdditionalInformation(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE)
    
    alcoholic_drink = models.BooleanField("Serve bebidas alcólicas")
    has_entertainment = models.BooleanField("Enterteinimento")
    has_thematicdecoration = models.BooleanField("Decoração Temática")
    has_childrenrides = models.BooleanField("Brinquedo pra Crianças")
    has_costumes = models.BooleanField("Fantasias para os Atores")
    has_parking = models.BooleanField("Estacionamento")
    has_externalarea = models.BooleanField("Área externa")
    has_music = models.BooleanField("Música")
    has_illumination = models.BooleanField("Iluminação")
    has_babychangingroom = models.BooleanField("Fraldário")

    def __str__(self):
        return "Additional Info of " + self.place.name



class PlaceVisualization(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    creation = models.DateTimeField(auto_now=True)






class PhotoProvisory(models.Model):
    photo = models.FileField('Foto', upload_to='place/photoprovisory')
    def __str__(self):
        return str(self.photo)


    def save(self): # Rewriting save to Resize

        if not self.id and not self.photo:
            return            

        super(PhotoProvisory, self).save()

        image = Image.open(self.photo)
        (width, height) = image.size

        if width > 700 or height > 700: # Needs resizing
            max_width_height = 400 # Max width or Height
            if max_width_height/width < max_width_height/height: # Height is bigger and will be resized
                factor = max_width_height/height
            else:
                factor = max_width_height/width
            size = ( int(width*factor), int(height*factor))
            image = image.resize(size, Image.ANTIALIAS)
            image = image.save(self.photo.path)



class PlacePhoto(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    photo = models.OneToOneField(PhotoProvisory, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.place.name)