import datetime, pytz

from django.views.generic import View
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from locacaoeventos.utils.main import *



class AboutUs(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "static/about_us.html", context)







class FAQ(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "static/faq.html", context)


    # No more post
    # def post(self, request, *args, **kwargs):
    #     context = base_context(request.user)
    #     email = request.POST.get("faq-form-email")
    #     text = request.POST.get("faq-form-question")


    #     str_titulo = ('Pergunta de USUÁRIO')
    #     str_body = ('De: ' + email + " >> " + text)
    #     send_mail(str_titulo, str_body, 'christian.org96@gmail.com', ["christian.org96@gmail.com"], fail_silently=False)


    #     context["sent_email"] = True
        return render(request, "static/faq.html", context)


class ContactUs(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        return render(request, "static/contact_us.html", context)


    def post(self, request, *args, **kwargs):
        context = base_context(request.user)
        email = request.POST.get("faq-form-email")
        text = request.POST.get("faq-form-question")

        name = request.POST.get("faq-form-name")
        cellphone = request.POST.get("faq-form-cellphone")
        str_titulo = ('Pergunta de USUÁRIO')
        str_body = (
            'De: ' + email + "\n" +
            "Nome:  " + name + "\n" +
            "Celular: " + cellphone + "\n" +
            "Mensagem: " + text + "\n"

        )
        send_mail(str_titulo, str_body, 'christian.org96@gmail.com', ["christian.org96@gmail.com"], fail_silently=False)


        context["sent_email"] = True
        return render(request, "static/contact_us.html", context)

