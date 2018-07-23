from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings

from locacaoeventos.apps.user.views_user import Home, Teste, Login, Logout, TermsConditions, ComingSoon, AboutUs
from locacaoeventos.apps.user.views import UploadFile, GetPhoto

import locacaoeventos.apps.user.urls
import locacaoeventos.apps.place.urls
import locacaoeventos.apps.user.urls_admin

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', ComingSoon.as_view()),
    url(r'^home/$', Home.as_view()),
    url(r'^teste/$', Teste.as_view()),
    url(r'^sobre-nos/$', AboutUs.as_view()),
    url(r'^termos-e-condicoes/$', TermsConditions.as_view()),

    url(r'^usuario/', include(locacaoeventos.apps.user.urls)),
    url(r'^buffet/', include(locacaoeventos.apps.place.urls)),
    url(r'^administrador/', include(locacaoeventos.apps.user.urls_admin)),
    url(r'^login/$', Login.as_view()),
    url(r'^logout/$', Logout.as_view()),


    url(r'^upload_file/$', UploadFile.as_view()),
    url(r'^get_photo/$', GetPhoto.as_view()),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
