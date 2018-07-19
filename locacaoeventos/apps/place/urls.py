from django.conf.urls import include, url

from locacaoeventos.apps.place.views import *

urlpatterns = [
    url(r'^listar/$', ListPlace.as_view()),
    url(r'^detalhar/$', DetailPlace.as_view()),
]
