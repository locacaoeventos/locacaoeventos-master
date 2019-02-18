from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import datetime
 
from django.core.mail import send_mail

logger = get_task_logger(__name__)
 




# A periodic task that will run every minute (the symbol "*" means every)
@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def scraper_send():
    str_titulo = str(datetime.datetime.now())
    str_body = "Verificação de mensagens não lidas, para envio de e-mail stá quase feito!!"
    to_email = "christian.hukai@gmail.com"
    send_mail(str_titulo, str_body, 'christian.org96@gmail.com', [to_email], fail_silently=False)
    # print("oi")
