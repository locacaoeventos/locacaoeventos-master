from django.contrib import admin
from .models import BuyerProfile, FamilyMember, ShoppingCart

admin.site.register(BuyerProfile)
admin.site.register(FamilyMember)
admin.site.register(ShoppingCart)
