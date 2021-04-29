
from bot.celery import app
from time import sleep
import telegram
from django.conf import settings

from .models import VipMembers

@app.task
def sendPeriodicMessage():
    for instance in VipMembers.objects.values('telegram_id').distinct():
        if (instance['telegram_id']):
            sendMessageFromBot.delay(instance['telegram_id'])


@app.task
def sendMessageFromBot(telegram_id, msg = "خوشحالیم که مارا انتخاب کرده اید"):
    bot = telegram.Bot(token=settings.TOKEN)
    bot.sendMessage(chat_id= telegram_id, text= msg)