from django.db.models.signals import post_save
from graphene_subscriptions.signals import post_save_subscription

from user.models import UserBot
from user.models import VipMembers

def VipMemberSaved(*args, **kwargs):
    print("VipMemberSaved")

post_save.connect(post_save_subscription, sender=UserBot)
post_save.connect(VipMemberSaved, sender=VipMembers)



