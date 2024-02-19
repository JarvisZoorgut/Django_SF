import logging

from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from newsportal.models import Subscriber, Post


logger = logging.getLogger(__name__)


def send_weekly_articles():
    # Находим всех подписчиков
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        # Получаем категорию подписчика
        category = subscriber.category

        # Находим все статьи в этой категории, опубликованные после последней отправки
        last_execution = DjangoJobExecution.objects.filter(
            job_id="send_weekly_articles", status=DjangoJobExecution.SUCCESS
        ).order_by("-run_time").first()

        if last_execution:
            last_execution_time = last_execution.run_time
        else:
            # Если не было предыдущих выполнений, отправляем все статьи
            last_execution_time = timezone.now() - timezone.timedelta(days=7)

        new_articles = Post.objects.filter(
            postCategory=category, dateCreation__gt=last_execution_time
        )

        if new_articles.exists():
            # Генерируем текст сообщения с новыми статьями
            subject = f'Контент за неделю в категории "{category}"'
            text_content = "Новый контент:\n\n"
            for article in new_articles:
                text_content += f'<a href="http://127.0.0.1:8000{article.get_absolute_url()}">{article.title}</a>'

            # Отправляем сообщение подписчику
            email = subscriber.user.email
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.send()

    logger.info("Weekly articles sent successfully!")


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=timezone.get_current_timezone())
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Добавляем задачу отправки статей каждую пятницу в 18:00
        scheduler.add_job(
            send_weekly_articles,
            trigger=CronTrigger(day_of_week="mon", hour="18", minute="18"),
            id="send_weekly_articles",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_articles'.")

        # Добавляем задачу удаления старых выполнений каждую неделю
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="sun", hour="0", minute="0"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")