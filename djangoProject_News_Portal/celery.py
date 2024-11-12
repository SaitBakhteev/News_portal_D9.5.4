import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'djangoProject_News_Portal.settings')
app = Celery('djangoProject_News_Portal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

