from django.conf.urls import include, url

from locacaoeventos.apps.user.views_admin import *
from django.contrib.auth.decorators import user_passes_test


urlpatterns = [
    url(r'^home/', user_passes_test(lambda u: u.has_perm('perm'))(AdminHome.as_view())),
    url(r'^upload-buffet/', user_passes_test(lambda u: u.has_perm('perm'))(UploadBuffet.as_view())),
]
