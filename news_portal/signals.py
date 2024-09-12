from django.db.models.signals import m2m_changed, post_init, pre_init, pre_save, post_save, post_delete
import django.db.models.signals as signals
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.conf import settings
from .models import Post, PostCategory, Category, UserSubcribes, Mail

@receiver(signal=m2m_changed, sender=PostCategory)
def notify_m2m_changed(sender, instance, action, **kwargs):
      if action == 'post_add':
          user_list = []  # список имен получателей и их почты уведомления о выходе новой публикации
          current_list=[] # текущий список для отслеживания добавился
                #  ли пользователь в список получатедей уведомления

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
                                          {'post': instance, 'username':i[0]})
              msg = EmailMultiAlternatives(subject=f'Выход новой публикации с названием {instance.title}',
                                               body='',
                                               from_email=settings.DEFAULT_FROM_EMAIL,
                                               to=[f'{i[1]}']
                                           )
              msg.attach_alternative(html, 'text/html')
              msg.send()
              Mail.objects.create(message=html, recepients_id=i[2], subject=instance.title)



