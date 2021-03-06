# -*- coding: utf-8 -*-
from .base import *

# Neste arquivo há mudanças específicas apenas para a fase de desenvolvimento

ALLOWED_HOSTS = ['*']

DEBUG = True
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# BROKER_URL = "amqp://locacao123f:locacaoqwe@localhost:22349/locacao123f"

# DEVELOPMENT CELERY RABBITMQ
BROKER_URL = "amqp://locacao123f:locacaoqwe@localhost:5672/locacao123f"
