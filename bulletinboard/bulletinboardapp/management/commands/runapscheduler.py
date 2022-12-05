import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import date, datetime,timedelta
from django.core.mail import EmailMultiAlternatives
logger = logging.getLogger(__name__)
 
 
# наша задача по выводу текста на экран
def my_job():
    subscribers = User.objects.all()
    users_active = []
    mydate = date.today()-timedelta(days=7)
    for sub_user in subscribers:
        if sub_user.subscribers_id not in users_active:
            recipient = User.objects.get(id = sub_user.subscribers_id)
            categorysId = SubsCategory.objects.filter(subscribers = sub_user.subscribers_id).values_list('category', flat=True) #.filter(created_at__gt = mydate)
            users_active.append(sub_user.subscribers_id)
            last_week = Post.objects.filter(created_at__gt = mydate, postCategory__in = categorysId)

            html_content = render_to_string( 
            'subs_mail_created.html',
            {
                'newMailSub': last_week,
            }
            )

            # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
            msg = EmailMultiAlternatives(
                subject= f'Dear subscriber - news from last week',
                body = last_week, #  это то же, что и message
                from_email='lexinet3g@gmail.com',
                to=[recipient.email], # это то же, что и recipients_list
                #fail_silently=False нуен что бы всё не полетело в тартарары если что-то пошло не так - обязательно в продакшене
            )
            msg.attach_alternative(html_content, "text/html") # добавляем html
            msg.send() # отсылаем
    
    print('hello from job')
 
 
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
            trigger=CronTrigger(second="*/1"),  # Тоже самое что и интервал, но задача тригера таким образом более понятна django
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