from celery import shared_task
import time
from django.http import HttpResponse
from .models import Comment
from datetime import datetime
from .models import Post
from datetime import timezone


@shared_task
def test_sleep():
    time.sleep(10)
    HttpResponse('Sleep task')

@shared_task
def hello_world():
    print("Hello world asynk")

@shared_task
def test_comments(post_id, user_id):
    time.sleep(10)
    post_date=Post.objects.get(id=post_id).create_time
    Comment.objects.create(user_id=user_id, comment_text=f'This is a comment created later than'
                                                   f'{datetime.now(tz=timezone.utc)-post_date}',
                                                        post_id=post_id)
