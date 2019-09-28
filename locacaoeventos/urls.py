from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from locacaoeventos.apps.user.views_general import *

from locacaoeventos.apps.user.views_general import Home, Teste, Login, Logout, TermsConditions, ComingSoon, AboutUs, GoDaddyVerification, Blog, Email
from locacaoeventos.apps.user.views import UploadFile, GetPhoto

import locacaoeventos.apps.user.urls
import locacaoeventos.apps.user.chat.urls
import locacaoeventos.apps.place.urls
import locacaoeventos.apps.user.urls_admin

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', ComingSoon.as_view()),
    url(r'^home/$', Home.as_view()),
    
    url(r'^blog/$', Blog.as_view()),
    url(r'^email/$', Email.as_view()),

    url(r'^email-buffet-recebe/$', EmailBuffetRecebe.as_view()),
    url(r'^email-cliente-recebe/$', EmailClienteRecebe.as_view()),
    url(r'^email-buffet-reserva/$', EmailBuffetReserva.as_view()),
    url(r'^email-buffet-cadastro/$', EmailBuffetCadastro.as_view()),
    url(r'^email-cliente-cadastro/$', EmailClienteCadastro.as_view()),
    url(r'^email-cliente-aguardo/$', EmailClienteAguardo.as_view()),
    url(r'^email-buffet-reserva-reforco/$', EmailBuffetReservaReforco.as_view()),

    url(r'^teste/$', Teste.as_view()),
    url(r'^sobre-nos/$', AboutUs.as_view()),
    url(r'^termos-e-condicoes/$', TermsConditions.as_view()),

    url(r'^usuario/', include(locacaoeventos.apps.user.urls)),
    url(r'^usuario/', include(locacaoeventos.apps.user.chat.urls)),
    url(r'^buffet/', include(locacaoeventos.apps.place.urls)),
    url(r'^administrador/', include(locacaoeventos.apps.user.urls_admin)),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),

    # Photos
    url(r'^upload_file/$', UploadFile.as_view()),
    url(r'^get_photo/$', GetPhoto.as_view()),

    # Django-Paypal
    # url(r'^paypal/', include('paypal.standard.ipn.urls')),

    url(r'^.well-known/pki-validation/godaddy.html$', GoDaddyVerification.as_view()),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
