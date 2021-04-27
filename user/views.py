from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .tasks import sendBotMessage

import logging
import json



@csrf_exempt
@require_POST
def webhookUserAdded(request):

    """
    Response to webhook request and set a worker to send message
    """

    data = json.loads(request.body)
    subData = json.loads(data['query'])
    phone_number = subData['billing']['phone']
    sendBotMessage.delay(phone_number=phone_number)
    print(phone_number)


    return HttpResponse(status=200)
    