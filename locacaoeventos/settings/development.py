# -*- coding: utf-8 -*-
from .base import *

# Neste arquivo há mudanças específicas apenas para a fase de desenvolvimento

ALLOWED_HOSTS = ['*']

DEBUG = False
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

BROKER_URL = 'amqp://guest:guest@localhost:22225//'
# BROKER_URL = "amqp://locacao123f:locacaoqwe@localhost:18941/locacao123f"
