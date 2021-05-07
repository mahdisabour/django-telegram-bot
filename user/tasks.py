
from bot.celery import app
from time import sleep
import telegram
from django.conf import settings

from .models import SiteBotMember

@app.task
def sendPeriodicMessage():
    for instance in SiteBotMember.objects.values('chat_id').distinct():
        if (instance['chat_id']):
            sendMessageFromBot.delay(instance['chat_id'])


@app.task
def sendMessageFromBot(chat_id, msg = "خوشحالیم که مارا انتخاب کرده اید"):
    bot = telegram.Bot(token=settings.TOKEN)
    bot.sendMessage(chat_id= chat_id, text= msg)