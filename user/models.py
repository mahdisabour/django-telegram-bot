from user.tasks import sendMessageFromBot
from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.fields import related
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return self.name


class SiteBotMember(models.Model):
    customer_id = models.BigIntegerField(primary_key=True)
    chat_id = models.BigIntegerField(blank=True, null=True)
    phone_number = models.CharField(
        blank=True, null=True, unique=True, max_length=11, validators=[MinLengthValidator(11)])
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"group : {self.group if self.group else 'None'}" + f" | phone_number : {self.phone_number}"


class Message(models.Model):
    message = models.TextField()
    timing = models.DateTimeField(auto_now=False, auto_now_add=False)
    receivers = models.ManyToManyField(SiteBotMember, related_name="messages")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return str(self.timing)



# there is bug here (if admin want to update user list, perhaps create redundancy message)
@receiver(post_save, sender=Message)
def sendMessage(sender, instance, created, **kwargs):
    receivers = instance.recievers.all()
    for receiver in receivers:
        if receiver.chat_id:
            sendMessageFromBot.apply_async(
                (receiver.chat_id, instance.message), eta=instance.timing)


class ProductPlan(models.Model):
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=500)
    owner = models.ForeignKey(
        SiteBotMember, on_delete=models.CASCADE, related_name='orders')
    plan = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.plan
