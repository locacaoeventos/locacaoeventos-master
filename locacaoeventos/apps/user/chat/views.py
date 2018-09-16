from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from locacaoeventos.utils.main import *
from locacaoeventos.utils.general import get_dic_by_key
from locacaoeventos.utils.place import *
from locacaoeventos.apps.user.chat.models import Message
from locacaoeventos.apps.place.placecore.models import PlacePhoto, Place

from itertools import chain
import datetime


class Chat(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        is_seller = request.GET.get("is_seller", False)
        if is_seller:
            template_base = "control_panel/seller_base.html"
        else:
            template_base = "control_panel/buyer_base.html"
        context["panel_type"] = "chat"
        context["template_base"] = template_base

        user = request.user

        # =================
        # Geting Messages
        messages_from = [{
            "user_contacted": message.user_to,
            "text": message.text,
            "datetime": message.datetime,
            "place": message.place,
            } for message in Message.objects.filter(user_from=user)
        ]
        messages_to = [{
            "user_contacted": message.user_from,
            "text": message.text,
            "datetime": message.datetime,
            "place": message.place,
            } for message in Message.objects.filter(user_to=user)
        ]

        messages = messages_from + messages_to
        if is_seller == True:
            for message in messages:
                message["photo"] = BuyerProfile.objects.get(user=message["user_contacted"]).photo

        else:
            for message in messages:
                message["photo"] = PlacePhoto.objects.filter(place=message["place"], is_first=True)[0].photo

            
        messages = sorted(messages, key=lambda k: k['datetime'], reverse=True) 
        messages_compiled = []
        for message in messages:
            if not get_dic_by_key(messages_compiled, "place", message["place"]):
                messages_compiled.append(message)
        # =================

        context["messages"] = messages_compiled

        return render(request, "chat.html", context)








class ChatView(View):
    def get(self, request, *args, **kwargs):
        context = base_context(request.user)
        if SellerProfile.objects.filter(user=request.user):
            context["template_base"] = "control_panel/seller_base.html"
        else:
            context["template_base"] = "control_panel/buyer_base.html"
        context["panel_type"] = "chat"

        context["place_pk"] = request.GET.get("place_pk")
        return render(request, "chat_view.html", context)

















class ChatGetViewAjax(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        buyerprofille = BuyerProfile.objects.get(user=user)

        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)
        sellerprofile = place.sellerprofile
        user_seller = sellerprofile.user

        messages = [{
            "message_text": message.text,
            "datetime": message.datetime,
            "from": buyerprofille.name,
            "photo": "/media/" + str(buyerprofille.photo),
            } for message in Message.objects.filter(user_from=user, user_to=user_seller, place=place)
        ] + [{
            "message_text": message.text,
            "datetime": message.datetime,
            "from": place.name,
            "place": place,
            } for message in Message.objects.filter(user_from=user_seller, user_to=user, place=place)
        ]
        if len(messages) > 0:
            messages = sorted(messages, key=lambda k: k['datetime'])



            # Sorting messages by groups
            messages_compiled = []
            message_dic = {
                "message_text": [messages[0]["message_text"]],
                "datetime": messages[0]["datetime"],
                "from": messages[0]["from"],
            }
            if "photo" in messages[0]:
                message_dic["photo"] = messages[0]["photo"]
            else:
                message_dic["photo"] = "/media/" + str(PlacePhoto.objects.filter(place=messages[0]["place"], is_first=True)[0].photo)
            if len(messages) == 1:
                messages_compiled.append(message_dic)


            previous_from = messages[0]["from"]
            count = 0
            for message in messages[1:]:
                if "photo" not in message:
                    message["photo"] = str(PlacePhoto.objects.filter(place=message["place"], is_first=True)[0].photo)
                if message["photo"] == None:
                    message["photo"] = "/static/img/icon/user.png"


                if previous_from != message["from"]:
                    messages_compiled.append(message_dic)
                    message_dic = {
                        "message_text": [message["message_text"]],
                        "datetime": message["datetime"],
                        "from": message["from"],
                        "photo": "/media/" + message["photo"],
                    }
                    previous_from = message["from"]
                else:
                    message_dic["message_text"].append(message["message_text"])

                    if count == len(messages[1:])-1:
                        messages_compiled.append(message_dic)


                count += 1
            data = {"messages":messages_compiled}
        else:
            data = {"messages": []}

        return JsonResponse(data)









class ChatGetDetailPlaceAjax(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        buyerprofille = BuyerProfile.objects.get(user=user)

        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)
        sellerprofile = place.sellerprofile
        user_seller = sellerprofile.user

        messages = [{
            "message_text": message.text,
            "datetime": message.datetime,
            "from": buyerprofille.name,
            "photo": "/media/" + str(buyerprofille.photo),
            } for message in Message.objects.filter(user_from=user, user_to=user_seller, place=place)
        ] + [{
            "message_text": message.text,
            "datetime": message.datetime,
            "from": place.name,
            "place": place,
            } for message in Message.objects.filter(user_from=user_seller, user_to=user, place=place)
        ]
        if len(messages) > 0:
            messages = sorted(messages, key=lambda k: k['datetime'])



            # Sorting messages by groups
            messages_compiled = []
            message_dic = {
                "message_text": [messages[0]["message_text"]],
                "datetime": messages[0]["datetime"],
                "from": messages[0]["from"],
            }
            if "photo" in messages[0]:
                message_dic["photo"] = messages[0]["photo"]
            else:
                message_dic["photo"] = "/media/" + str(PlacePhoto.objects.filter(place=messages[0]["place"], is_first=True)[0].photo)
            if len(messages) == 1:
                messages_compiled.append(message_dic)


            previous_from = messages[0]["from"]
            count = 0
            for message in messages[1:]:
                if "photo" not in message:
                    message["photo"] = str(PlacePhoto.objects.filter(place=message["place"], is_first=True)[0].photo)
                if message["photo"] == None:
                    message["photo"] = "/static/img/icon/user.png"


                if previous_from != message["from"]:
                    messages_compiled.append(message_dic)
                    message_dic = {
                        "message_text": [message["message_text"]],
                        "datetime": message["datetime"],
                        "from": message["from"],
                        "photo": "/media/" + message["photo"],
                    }
                    previous_from = message["from"]
                else:
                    message_dic["message_text"].append(message["message_text"])

                    if count == len(messages[1:])-1:
                        messages_compiled.append(message_dic)


                count += 1
            data = {"messages":messages_compiled}
        else:
            data = {"messages": []}

        return JsonResponse(data)







class ChatSendAjax(View):
    def get(self, request, *args, **kwargs):
        text = request.GET.get("message_text")
        place_pk = request.GET.get("place_pk")
        place = Place.objects.get(pk=place_pk)
        user = request.user

        now = datetime.datetime.now()

        
        message = Message.objects.create(
            text = text,
            user_from = user,
            user_to = place.sellerprofile.user,
            datetime = now,
            place = place
        )

        data = {"check": "check"}
        return JsonResponse(data)




