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

# test




# Url for telegram bot
botUrl = settings.BOT_URL





# package site and bot 
@csrf_exempt
@require_POST
def orderCreated(request):
    """
    Response to webhook request and set a worker to send message
    """
    try:
        data = json.loads(request.body)
        # subData = json.loads(data['query'])
        # This if for test
        customer_id = data['customer_id']
        phone_number = data['billing']['phone']
        if(SiteBotMember.objects.filter(customer_id=customer_id, phone_number=phone_number).exists()):
            user = SiteBotMember.objects.get(customer_id=customer_id)
            if user.chat_id:
                sendMessageFromBot.delay(chat_id=user.chat_id, msg= "سفارش شما با موفقیت ثبت شد")
                content = {
                    "Message": "خوشبختانه شما در بات ثبت نام کرده اید . از خدمات ان لذت ببرید"
                }
            else:
                content = {
                    "Message": "لطفا برای داشتن خدمات اضافی در بات ثبت نام کنید",
                    "botUrl": botUrl
                }
        else:
            if (SiteBotMember.objects.filter(phone_number=phone_number).exists()):
                user = SiteBotMember.objects.get(phone_number=phone_number)
                if (not user.chat_id):
                    content = {
                        "Message": "این شماره قبلا در بات ثبت نام کرده است",
                    }
            else:
                SiteBotMember(customer_id=customer_id, phone_number=phone_number).save()
                content = {
                    "Message": "لطفا برای داشتن خدمات اضافی در بات ثبت نام کنید",
                    "botUrl": botUrl
                }

        return JsonResponse(content, status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=200)

    

