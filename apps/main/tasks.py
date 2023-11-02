import requests
from django.conf import settings
from .models import Message
from celery import shared_task


@shared_task(bind=True)
def task_message_delete(self, *args, **kwargs):
    t_id = kwargs.get('t_id')
    ms = Message.objects.filter(travel_id=t_id)
    for i in ms:
        requests.get(
            url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/deleteMessage",
            params={"chat_id": i.chat_id, "message_id": i.message_id})
        i.delete()
    return 'Deleted'


@shared_task(bind=True)
def task_travel(self, *args, **kwargs):
    name = kwargs.get('name')
    phone = kwargs.get('phone')
    username = kwargs.get('username')
    note = kwargs.get('note')
    lst = kwargs.get('lst')
    to_where = kwargs.get('to_where')
    where = kwargs.get('where')
    lat = kwargs.get('lat')
    lon = kwargs.get('lon')
    t_id = kwargs.get('t_id')
    count_person = kwargs.get('count_person')
    txt = f"👨‍💼 Yo’lovchi: <b>{name}</b>\n"
    txt += f"☎️ Telefon: <b>+{phone}</b>\n"
    txt += f"🗺️ Yunalish: <b>{where} -> {to_where}</b>\n"
    txt += f"👥 Yo'lovchilar soni: <b>{count_person}</b>\n"
    txt += f"🇺🇿 Telegram: <b>{username}</b>\n"
    txt += f"⌨️ Qo'shimcha: <b>{note}</b>\n"
    txt += f"📍 Yo’lga chiqish lokatsiyasi: 👇️\n"
    for i in lst:
        r = requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
                         params={'text': txt, 'chat_id': i, 'parse_mode': "HTML"})
        rt = requests.get(url=f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendLocation",
                          params={'latitude': lat, 'longitude': lon, 'chat_id': i})
        try:
            rs = r.json()
            mes_id = rs['result']['message_id']
            chat_id = rs['result']['chat']['id']
            Message.objects.create(travel_id=t_id, chat_id=chat_id, message_id=mes_id)
            lc = rt.json()
            mes_id = lc['result']['message_id']
            chat_id = lc['result']['chat']['id']
            Message.objects.create(travel_id=t_id, chat_id=chat_id, message_id=mes_id)
        except Exception as e:
            print(e)
    return 'Sent'
