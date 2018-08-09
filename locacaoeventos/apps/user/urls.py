from django.conf.urls import include, url

from locacaoeventos.apps.user.views_user import *
from locacaoeventos.apps.user.views_control_panel_seller import *
from locacaoeventos.apps.user.views_control_panel_buyer import *
from locacaoeventos.apps.user.views_admin import *
from locacaoeventos.apps.user.views import *
from locacaoeventos.apps.place.views import *


urlpatterns = [
    # User General
    url(r'^cadastrar/$', CreateUser.as_view()),
    url(r'^cadastro-concluido/$', CreateUserCompleted.as_view()),
    url(r'^esqueceu-senha/$', ForgotPassword.as_view()),
    url(r'^confirmar-email/$', ConfirmEmail.as_view()),
    url(r'^trocar-senha/$', ChangePassword.as_view()),

    # Seller - General
    url(r'^anunciante/conta/$', EditSeller.as_view()),
    url(r'^anunciante/buffet/listar/$', ListPlaceOwned.as_view()),
    url(r'^anunciante/buffet/cadastrar/$', CreateEditPlace.as_view()),

    # Seller - Availability
    url(r'^anunciante/buffet/disponibilidade/$', AvailabilityPlace.as_view()),
    url(r'^ajax/unavailability/create/$', UnavailabilityCreateAjax.as_view()),
    url(r'^ajax/unavailability/detail/$', UnavailabilityDetailAjax.as_view()),

    # Buyer
    url(r'^conta/$', EditBuyer.as_view()),
    url(r'^buffets-agendados/$', ListPlaceBought.as_view()),
    url(r'^avaliar-buffet/$', ReviewPlaceBought.as_view()),


    # General
    url(r'^calendarioexemplo/$', CalendarExample.as_view()),
    url(r'^ajax/calendario/$', CalendarAjax.as_view()),
    url(r'^ajax/familymember/create-delete/$', CreateDeleteFamilyMemberAjax.as_view()),
    

]
