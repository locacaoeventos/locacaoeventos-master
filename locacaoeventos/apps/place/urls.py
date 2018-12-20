from django.conf.urls import include, url

from locacaoeventos.apps.place.views import *
from locacaoeventos.apps.place.views_maps import *
from locacaoeventos.apps.place.views_buying_flux import *
from locacaoeventos.apps.place.views_ajax import *


# /buffet/
urlpatterns = [
    url(r'^listar/$', ListPlace.as_view()),
    url(r'^detalhar/$', DetailPlace.as_view()),
    url(r'^comprar/$', BuyPlace.as_view()),
    url(r'^finalizar-compra/$', PurchasePlace.as_view(), name="checkout"),

    url(r'^ajax/get/$', ListBuffetAjax.as_view()),
    url(r'^ajax/order-by/$', OrderByBuffetAjax.as_view()),
    url(r'^ajax/get-place/$', GetPlaceInformation.as_view()),
    url(r'^ajax/love/$', LoveBuffetAjax.as_view()),
    

    url(r'^mapa/$', MapsPlace.as_view()),
    url(r'^maps-ajax/$', MapsPlaceAjax.as_view()),

]
