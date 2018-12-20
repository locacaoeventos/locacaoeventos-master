from django.contrib import admin
from .models import Place, PlaceAdditionalInformation, PlaceVisualization, PlacePhoto, PhotoProvisory, PlaceFeature, PlaceLove

admin.site.register(Place)
admin.site.register(PlaceAdditionalInformation)
admin.site.register(PlaceVisualization)
admin.site.register(PlacePhoto)
admin.site.register(PhotoProvisory)
admin.site.register(PlaceFeature)
admin.site.register(PlaceLove)
