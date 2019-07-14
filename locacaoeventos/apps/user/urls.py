from django.conf.urls import include, url

from locacaoeventos.apps.user.views_user import *
from locacaoeventos.apps.user.views_general import *
from locacaoeventos.apps.user.views_calendar import *
from locacaoeventos.apps.user.views_control_panel_seller import *
from locacaoeventos.apps.user.views_control_panel_seller_ajax import *
from locacaoeventos.apps.user.views_control_panel_buyer import *
from locacaoeventos.apps.user.views_control_panel_general import *
from locacaoeventos.apps.user.views_admin import *
from locacaoeventos.apps.user.views_static import *
from locacaoeventos.apps.user.views import *
from locacaoeventos.apps.place.views import *


urlpatterns = [
    # User General
    url(r'^cadastrar/$', CreateUser.as_view()),
    url(r'^cadastro-concluido/$', CreateUserCompleted.as_view()),
    url(r'^cadastrar-facebook/$', CreateUserFacebook.as_view()),
    url(r'^esqueceu-senha/$', ForgotPassword.as_view()),
    url(r'^confirmar-email/$', ConfirmEmail.as_view()),
    url(r'^trocar-senha/$', ChangePassword.as_view()),

    # Seller - General
    url(r'^anunciante/conta/$', EditSeller.as_view()),
    url(r'^anunciante/buffet/listar/$', ListPlaceOwned.as_view()),
    url(r'^anunciante/buffet/cadastrar/$', CreateEditPlace.as_view()),

    # Seller - Availability
    url(r'^anunciante/buffet/disponibilidade/$', AvailabilityPlace.as_view()),
    url(r'^ajax/unavailability/get/$', UnavailabilityGetAjax.as_view()),
    url(r'^ajax/unavailability/create/$', UnavailabilityCreateAjax.as_view()),
    url(r'^ajax/unavailability/detail/$', UnavailabilityDetailAjax.as_view()),
    url(r'^ajax/unavailability/delete/$', UnavailabilityDeleteAjax.as_view()),
    url(r'^ajax/placeprice/get/$', PlacePriceGetAjax.as_view()),
    url(r'^ajax/placeprice/create/$', PlacePriceCreateAjax.as_view()),
    url(r'^ajax/placeprice/delete/$', PlacePriceDeleteAjax.as_view()),
    url(r'^ajax/sazonality/create/$', SazonalityCreateAjax.as_view()),
    url(r'^ajax/sazonality/get/$', SazonalityGetAjax.as_view()),
    url(r'^ajax/sazonality/delete/$', SazonalityDeleteAjax.as_view()),

    # Buyer
    url(r'^conta/$', EditBuyer.as_view()),
    # url(r'^familia/$', FamilyMemberEdit.as_view()),
    url(r'^buffets-agendados/$', ListPlaceBought.as_view()),
    url(r'^avaliar-buffet/$', ReviewPlaceBought.as_view()),
    url(r'^familia/$', FamilyBuyer.as_view()),

    # User General
    url(r'^favoritos/$', UserLoved.as_view()),

    # General
    url(r'^calendarioexemplo/$', CalendarExample.as_view()),
    url(r'^ajax/calendario/$', CalendarAjax.as_view()),
    url(r'^ajax/calendario-input/$', CalendarInputAjax.as_view()),
    url(r'^ajax/familymember/create-delete/$', CreateDeleteFamilyMemberAjax.as_view()),
    url(r'^ajax/calendario-sazonalidade/$', CalendarSeasonAjax.as_view()),
    


    # Static
    url(r'^sobre-nos/$', AboutUs.as_view()),
    url(r'^faq/$', FAQ.as_view()),
    url(r'^fale-conosco/$', ContactUs.as_view()),

]
