from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import SiteBotMember
from .tasks import sendMessageFromBot

from django.conf import settings

import logging
import json




# Url for telegram bot
botUrl = settings.BOT_URL



# package site and bot 
@csrf_exempt
@require_POST
def orderCreated(request):
    """
    Response to webhook request and set a worker to send message
    """
    data = json.loads(request.body)
    subData = json.loads(data['query'])
    # This if for test
    customer_id = subData['customer_id']
    phone_number = subDate['billing']['phone']
    if(SiteBotMember.objects.filter(customer_id=customer_id).exists()):
        user = SiteBotMember.objects.get(customer_id=customer_id)
        if user.chat_id:
            sendMessageFromBot.delay(telegram_id=user.chat_id, msg= f"{user.chat_id}")
            content = {
                "Message": "خوشبختانه شما در بات ثبت نام کرده اید . از خدمات ان لذت ببرید"
            }
        else:
            content = {
                "Message": "لطفا برای داشتن خدمات اضافی در بات ثبت نام کنید",
                "botUrl": botUrl
            }
    else:
        SiteBotMember(customer_id=customer_id, phone_number=phone_number).save()
        content = {
            "Message": "لطفا برای داشتن خدمات اضافی در بات ثبت نام کنید",
            "botUrl": botUrl
        }

    return JsonResponse(content, status=200)
    

