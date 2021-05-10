from bot.celery import app
from time import sleep
import telegram
from django.conf import settings
import datetime

from .models import SiteBotMember, ProductPlan


@app.task
def sendPeriodicMessage():
    for instance in SiteBotMember.objects.values('chat_id').distinct():
        if (instance['chat_id']):
            sendMessageFromBot.delay(instance['chat_id'])


@app.task
def sendMessageFromBot(chat_id, msg="خوشحالیم که مارا انتخاب کرده اید"):
    bot = telegram.Bot(token=settings.TOKEN)
    bot.sendMessage(chat_id=chat_id, text=msg)


# cheking expirations and send them message
@app.task
def checkExpireDate():
    for user in SiteBotMember.objects.all():
        if not hasValidExpire(user.orders.first().expiration_date): # send message to user if True
            sendExpirationMsgToUser.delay(chat_id=user.chat_id)
        if overFlowTime(user.orders.first().expiration_date): # delete user if true
            deleteExpiredUser(user)


# check expirations date to send them message
def hasValidExpire(date):
    if datetime.date.today() > date - datetime.timedelta(days=4):
        return False
    return True


# check time to kill user
def overFlowTime(date):
    if datetime.date.today() > date :
        return True
    return False


@app.task
def sendExpirationMsgToUser(chat_id):
    msg = "زمان استفاده از محصول شما رو به پایان است"
    sendMessageFromBot.delay(chat_id=chat_id, msg=msg)


@app.task
def deleteExpiredUser(user):
    chat_id = user.chat_id
    user.delete()
    msg = "شما دیگر از خدمات بات بهره مند نیستید"
    sendMessageFromBot.delay(chat_id=chat_id, msg=msg)
