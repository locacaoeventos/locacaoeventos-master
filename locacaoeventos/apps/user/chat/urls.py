from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from locacaoeventos.apps.user.chat.views import *



urlpatterns = [
    url(r'^chat/$', login_required(Chat.as_view())),
    url(r'^chat/visualizar/$', login_required(ChatView.as_view())),

    
    url(r'^chat/contact/$', login_required(ChatSendAjax.as_view())),
    url(r'^chat/get-visualizar/$', login_required(ChatGetViewAjax.as_view())),

    # url(r'^chat/get-place-detail/$', ChatGetDetailPlaceAjax.as_view()),

]
