import logging
from django.contrib.auth.models import User
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import date, datetime,timedelta
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from bulletinboardapp.models import Ad
logger = logging.getLogger(__name__)
 

def my_job():
    mydate = date.today()-timedelta(days=7)
    users = User.objects.all()
    last_week_ads = Ad.objects.filter(created_ad__gt = mydate)
    for sub_user in users:
        if not sub_user.email.strip():
            continue
        html_content = render_to_string( 
        'newsletter.html',
        {
            'newMailSub': last_week_ads,
        }
        )

        msg = EmailMultiAlternatives(
            subject= f'Dear {sub_user.first_name}, we have prepared a selection for you ads from last week',
            body = str(last_week_ads),
            from_email='lexinet3g@gmail.com',
            to=[sub_user.email], 
            #fail_silently=False нуен что бы всё не полетело в тартарары если что-то пошло не так - обязательно в продакшене
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        msg.send() 

 
 
# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")