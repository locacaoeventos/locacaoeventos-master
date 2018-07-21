from django.views.generic import View
from django.shortcuts import render, redirect

from locacaoeventos.utils.main import *


class AdminHome(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "admin/home.html", context)


class AdminLocacao(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "admin/home.html", context)



class UploadBuffet(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "admin/upload_buffet.html", context)




