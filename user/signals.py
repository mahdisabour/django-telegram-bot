from django.db.models.signals import post_save
from graphene_subscriptions.signals import post_save_subscription

from user.models import UserBot


post_save.connect(post_save_subscription, sender=UserBot)