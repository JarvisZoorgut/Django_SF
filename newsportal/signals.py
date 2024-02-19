from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post


@receiver(m2m_changed, sender=Post.postCategory.through)
def product_created(instance, action, **kwargs):
    if action!= 'post_add':
        return

    # Получаем все категории, связанные с этим экземпляром поста
    categories = instance.postCategory.all()

    # Получаем список всех пользователей, подписанных на эти категории
    emails = User.objects.filter(
        subscribers__category__in=categories
    ).values_list('email', flat=True)

    subject = f'Новый контент в категории {", ".join([category.name for category in categories])}'

    text_content = (
        f'Контент: <a href="http://127.0.0.1:8000{instance.get_absolute_url()}">{instance.title}</a>'
    )
    html_content = (
        f'Контент: <a href="http://127.0.0.1:8000{instance.get_absolute_url()}">{instance.title}</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()