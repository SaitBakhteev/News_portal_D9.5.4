from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category, PostCategory, User, UserSubcribes, Mail, Comment
import time
from django.http import HttpResponse
from datetime import datetime
from datetime import timezone
from datetime import timedelta

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


@shared_task
def send_notify_to_subscribers(instance_id):  # функция отправки уведомлений о выходе новой статьи подписчикам категорий
    user_list = []  # список имен получателей и их почты уведомления о выходе новой публикации
    current_list = []  # текущий список для отслеживания добавился
    #  ли пользователь в список получателей уведомления
    instance = Post.objects.get(id=instance_id)  # присвоение по id новой статьи

    for category in PostCategory.objects.filter(post_id=instance_id):
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
def weekly_mailing():  # еженедельная рассылка уведомлений о последних публикациях за неделю
    delta=datetime.now (timezone.utc)-timedelta(days=7)
    posts=Post.objects.filter(create_time__gte=delta)
    post_pk=Post.objects.filter(create_time__gte=delta).values_list('pk',flat=True)
    categories=set(Category.objects.filter(post__in=posts))
    user_pk=set(User.objects.filter(category__in=categories).values_list('pk',flat=True))

    for user in User.objects.filter(pk__in=user_pk):
        post_list = []  # список постов для еженедльной рассылки полдписчикам
        current_post_list = []  # список для отслеживания добавляемых постов в post_list во избежание
        # дублирования во время рассылки одному и тому же подписчику
        for post in Post.objects.filter(pk__in=post_pk, category__in=categories, category__usersubcribes__subcribe=user):
            if post not in current_post_list:
                current_post_list.append(post)
                post_list.append(post)

        html=render_to_string('flatpages/mail/scheduler_message.html',
                              {'username':user.username,'post':post_list})
        msg=EmailMultiAlternatives(subject='Список публикаций за неделю подписчикам ',
                                   body='',
                                   from_email=settings.DEFAULT_FROM_EMAIL,
                                   to=[f'{user.email}'])
        msg.attach_alternative(html,'text/html')
        msg.send()


    return 0
