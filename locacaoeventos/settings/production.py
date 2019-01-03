# -*- coding: utf-8 -*-

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'locacao_eventos3',
         'USER': 'locacao123f',
         'PASSWORD': 'locacaoqwe',
         'HOST': '127.0.0.1',
         'PORT': '5432',
    }
}

# Static files
STATICFILES_DIRS = (
    '/home/locacao123f/webapps/locacao_eventos/locacaoeventos-master/locacaoeventos/static/',
)

STATIC_ROOT = '/home/locacao123f/webapps/locacao_eventos_static/'
# MEDIA_ROOT = '/home/catalizr/webapps/catalizrv1_media/'

# Comando 'python manage.py collectstatic' copiara arquivos deste caminho para
# o caminho do STATIC_ROOT
# STATICFILES_DIRS = (
#     '/home/nexohw/webapps/sinexo2/si_nexo/nexo_si/static/',
# )

# Media files
# MEDIA_ROOT = '/home/nexohw/webapps/si_nexo_media/'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, "templates")],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'nexo_si.apps.atores.views_crud.notificacoes',
#             ],
#         },
#     },
# ]


# Código abaixo gera log de erro em ~/logs/user/
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         },
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#             }
#     },
# }





# CELERY
# BROKER_URL = 'amqp://guest:guest@localhost:22225//'
# BROKER_URL = "amqp://locacao123f:locacaoqwe@localhost:5672/locacao123f"
BROKER_URL = "amqp://locacao123f:locacaoqwe@localhost:22349/locacao123f"
