from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.


class SiteBotMember(models.Model):
    customer_id = models.BigIntegerField(primary_key=True)
    chat_id = models.BigIntegerField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, unique=True, max_length=11, validators=[MinLengthValidator(11)])


    def __str__(self):
        return f"{self.customer_id}"
    