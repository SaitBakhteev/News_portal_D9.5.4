from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PostCategory
from .tasks import send_notify_to_subscribers


@receiver(signal=m2m_changed, sender=PostCategory)
def notify_m2m_changed(sender, instance, action, **kwargs):
      if action == 'post_add':
            send_notify_to_subscribers.delay(instance.id)
