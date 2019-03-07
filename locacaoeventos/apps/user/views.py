from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from locacaoeventos.utils.forms import PhotoProvisoryForm
from locacaoeventos.utils.main import base_context
from locacaoeventos.utils.datetime import test_date
from locacaoeventos.apps.place.placecore.models import Place, PlacePhoto, PhotoProvisory
from locacaoeventos.apps.user.buyerprofile.models import BuyerProfile, FamilyMember








class UploadFile(View):
    def post(self, request):
        form = PhotoProvisoryForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            photo = form.save()
            data = {
                'is_valid': True,
                'name': photo.photo.name,
                'url': photo.photo.url,
                'pk': photo.pk
            }
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class GetPhoto(View):
    def get(self, request):
        photos_list = request.GET.get("photos_list").split(",")
        photos = []
        for i in range(len(photos_list)):
            photo_provisory = PhotoProvisory.objects.get(pk=photos_list[i])
            photos.append({
                "url":str(photo_provisory.photo),
                "pk":str(photo_provisory.pk)
            })
        data = {"photos":photos}
        return JsonResponse(data)





class CreateDeleteFamilyMemberAjax(View):
    def get(self, request):
        data = {}


        familymember_pk = request.GET.get("familymember_pk", None)
        if familymember_pk: # Deletes
            data = {"familymember_pk":familymember_pk}
            familymember = FamilyMember.objects.get(pk=familymember_pk)
            familymember.delete()

        else: # Creates
            familymember_gender = request.GET.get("familymember_gender")
            familymember_birthday = request.GET.get("familymember_birthday")
            familymember_name = request.GET.get("familymember_name")
            familymember_relation = request.GET.get("familymember_relation")

            if not test_date(familymember_birthday):
                data["error"] = True

            else:
                familymember = FamilyMember.objects.create(
                    name = familymember_name,
                    gender = familymember_gender,
                    birthday = familymember_birthday,
                    relation = familymember_relation,
                    related_to = BuyerProfile.objects.get(user=request.user)
                )
                data = {
                    "familymember_gender": familymember_gender,
                    "familymember_birthday": familymember_birthday,
                    "familymember_name": familymember_name,
                    "familymember_relation": familymember_relation,
                    "pk": familymember.pk
                }

        return JsonResponse(data)







