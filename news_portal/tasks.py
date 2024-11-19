from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post, PostCategory, UserSubcribes, Mail, Comment
import time
from django.http import HttpResponse
from datetime import datetime
from datetime import timezone


@shared_task
def send_notify_to_subscribers(instance):  # функция отправки уведомлений о выходе новой статьи подписчикам категорий
    user_list = []  # список имен получателей и их почты уведомления о выходе новой публикации
    current_list = []  # текущий список для отслеживания добавился
    #  ли пользователь в список получателей уведомления

    for category in PostCategory.objects.filter(post=instance):
        for subscriber in UserSubcribes.objects.filter(category=category.category):
            username, email, pk = (subscriber.subcribe.username,
                                   subscriber.subcribe.email,
                                   subscriber.subcribe.pk)
            if email not in current_list:
                current_list.append(email)
                user_list.append((username, email, pk))
    for i in user_list:
        html = render_to_string('flatpages/mail/send_html_mail.html',
                                {'post': instance, 'username': i[0]})
        msg = EmailMultiAlternatives(subject=f'Выход новой публикации с названием {instance.title}',
                                     body='',
                                     from_email=settings.DEFAULT_FROM_EMAIL,
                                     to=[f'{i[1]}']
                                     )
        msg.attach_alternative(html, 'text/html')
        msg.send()
        Mail.objects.create(message=html, recepients_id=i[2], subject=instance.title)


@shared_task
def test_sleep():
    time.sleep(10)
    HttpResponse('Sleep task')


@shared_task
def hello_world():
    print("Hello world async")


@shared_task
def test_comments(post_id, user_id):
    time.sleep(10)
    post_date = Post.objects.get(id=post_id).create_time
    Comment.objects.create(user_id=user_id, comment_text=f'This is a comment created later than'
                                                         f'{datetime.now(tz=timezone.utc)-post_date}',
                           post_id=post_id)
