from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import SiteBotMember, ProductPlan
from .tasks import sendMessageFromBot

from django.conf import settings

import logging
import json
import datetime 
from dateutil.relativedelta import relativedelta

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
                content = {
                    "Message": "این شماره قبلا در بات ثبت نام کرده است",
                }

            else:
                SiteBotMember(customer_id=customer_id, phone_number=phone_number).save()
                content = {
                    "Message": "لطفا برای داشتن خدمات اضافی در بات ثبت نام کنید",
                    "botUrl": botUrl
                }

        try:
            user = SiteBotMember.objects.get(customer_id=customer_id, phone_number=phone_number)
            for product in data['line_items']:
                name = product['name']
                plan = product['sku']

                # ["amount", "type"]
                subPlan = plan.split('_')
                product_id = product['product_id']
                days = int(subPlan[0]) if subPlan[-1] == 'days' else int(subPlan[0])*30
                if (ProductPlan.objects.filter(product_id=product_id).exists()):
                    ProductPlan.objects.get(product_id=product_id).expiration_date = datetime.date.today()+datetime.timedelta(days=days)
                else:
                    ProductPlan(product_id=product_id, product_name=name, expiration_date=datetime.date.today()+datetime.timedelta(days=days), owner=user, plan=plan).save()
        except Exception as e:
            print(e)

        return JsonResponse(content, status=200)
    except Exception as e:
        print(e)
        return HttpResponse(status=200)

    

