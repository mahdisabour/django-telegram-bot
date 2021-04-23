"""
ASGI config for bot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot.settings')
django.setup()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from user.consumer import BotConsumer
from django.urls import re_path, path
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer





application = ProtocolTypeRouter({
  "websocket": AuthMiddlewareStack(
        URLRouter([
            path("graphql/", GraphqlSubscriptionConsumer),
        ])
    ),
})

