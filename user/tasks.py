
from bot.celery import app
from time import sleep


@app.task
def sendBotMessage(phone_number):
    sleep(5)
    print(phone_number)    