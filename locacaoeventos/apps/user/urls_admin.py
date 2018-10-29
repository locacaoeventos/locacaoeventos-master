from django.conf.urls import include, url

from locacaoeventos.apps.user.views_admin import *
from django.contrib.auth.decorators import user_passes_test

from locacaoeventos.apps.user.views_admin_ajax import *

urlpatterns = [
    url(r'^home/$', user_passes_test(lambda u: u.has_perm('perm'))(AdminHome.as_view())),

    url(r'^listar-buffet/$', user_passes_test(lambda u: u.has_perm('perm'))(AdminListBuffet.as_view())),
    url(r'^verificar-buffet/$', user_passes_test(lambda u: u.has_perm('perm'))(AdminVerifyBuffet.as_view())),
    url(r'^destaque-buffet/$', user_passes_test(lambda u: u.has_perm('perm'))(AdminFeaturedBuffet.as_view())),

    url(r'^upload-buffet/$', user_passes_test(lambda u: u.has_perm('perm'))(UploadBuffet.as_view())),



    # AJAX
    url(r'^ban-buffet/$', ListBuffetBan.as_view()),
    url(r'^verificar-buffet-ajax/$', VerifyBuffet.as_view()),
]
