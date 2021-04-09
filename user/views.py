from django.shortcuts import render
from bot.hanelBot import TelegramBot
from django.http import HttpResponse
# Create your views here.


def teleBot(request):
    bot = TelegramBot()
    bot.runBot()
    return HttpResponse("test")
    
