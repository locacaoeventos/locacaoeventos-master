from django.conf.urls import include, url

from locacaoeventos.apps.user.views_user import *
from locacaoeventos.apps.user.views_control_panel_seller import *
from locacaoeventos.apps.user.views_control_panel_buyer import *
from locacaoeventos.apps.user.views_admin import *
from locacaoeventos.apps.user.views import *
from locacaoeventos.apps.place.views import *


urlpatterns = [
    url(r'^cadastrar/$', CreateUser.as_view()),
    url(r'^cadastro-concluido/$', CreateUserCompleted.as_view()),
    url(r'^esqueceu-senha/$', ForgotPassword.as_view()),
    url(r'^confirmar-email-comprador/$', ConfirmEmailBuyer.as_view()),
    url(r'^trocar-senha/$', ChangePassword.as_view()),


    url(r'^anunciante/conta/$', EditSeller.as_view()),
    url(r'^anunciante/buffet/listar/$', ListPlaceOwned.as_view()),
    url(r'^anunciante/buffet/cadastrar/$', CreatePlace.as_view()),

    url(r'^conta/$', EditBuyer.as_view()),
    url(r'^buffets-agendados/$', ListPlaceBought.as_view()),
    url(r'^avaliar-buffet/$', ReviewPlaceBought.as_view()),

    url(r'^calendarioexemplo/$', CalendarExample.as_view()),
    url(r'^ajax/calendario/$', CalendarAjax.as_view()),





    # Admin
    url(r'^admin_locacao/$', AdminLocacao.as_view()),
]
