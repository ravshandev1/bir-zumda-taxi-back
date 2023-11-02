from celery import shared_task
import requests
from django.conf import settings


@shared_task(bind=True)
def task_ads(self, *args, **kwargs):
    image = kwargs.get('image')
    video = kwargs.get('video')
    text = kwargs.get('text')
    lst = kwargs.get('lst')
    for i in lst:
        if image:
            requests.post(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendPhoto",
                          params={'chat_id': i, 'caption': text, 'parse_mode': "HTML"},
                          files={'photo': open(image, 'rb')})
        elif video:
            requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendVideo",
                         params={'chat_id': i, 'caption': text, 'parse_mode': "HTML"},
                         files={'video': open(video, 'rb')})
        else:
            requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
                         params={'text': text, 'chat_id': i, 'parse_mode': "HTML"})
    return 'Sent'
