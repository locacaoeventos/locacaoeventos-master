from django.conf.urls import include, url

from locacaoeventos.apps.user.chat.views import *



urlpatterns = [
    url(r'^chat/$', Chat.as_view()),
    url(r'^chat/visualizar/$', ChatView.as_view()),

    
    url(r'^chat/contact/$', ChatSendAjax.as_view()),
    # url(r'^chat/get-place-detail/$', ChatGetDetailPlaceAjax.as_view()),
    url(r'^chat/get-visualizar/$', ChatGetViewAjax.as_view()),
]
