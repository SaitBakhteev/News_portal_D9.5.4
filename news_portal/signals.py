from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import PostCategory, Post
from .tasks import send_notify_to_subscribers
from pprint import pprint

@receiver(signal=m2m_changed, sender=PostCategory)
def notify_m2m_changed(sender, instance, action, **kwargs):
      if action == 'post_add':
            send_notify_to_subscribers.delay(instance.id)

@receiver(signal=post_save, sender=Post)
def update_post(sender, instance, action, **kwargs):
      if action == 'post_update':
            pprint(f'{instance.title} - {instance.pk}')