from celery import Celery
from django.conf import settings

from django.core.mail import send_mail

app = Celery('tasks', broker=settings.BROKER_URL)


@app.task
def test(x, y):
    str_titulo = "afwaefwea"
    str_body = "aewrwefawefwe"
    to_email = "christian.hukai@gmail.com"
    send_mail(str_titulo, str_body, 'christian.org96@gmail.com', [to_email], fail_silently=False)
    return x + y



