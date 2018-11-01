from django.conf.urls import include, url

from locacaoeventos.apps.place.views import *
from locacaoeventos.apps.place.views_ajax import *

urlpatterns = [
    url(r'^listar/$', ListPlace.as_view()),
    url(r'^detalhar/$', DetailPlace.as_view()),

    url(r'^ajax/get/$', ListBuffetAjax.as_view()),
    url(r'^ajax/order-by/$', OrderByBuffetAjax.as_view()),
    url(r'^ajax/get-place/$', GetPlaceInformation.as_view()),
    


]
