from django.db import models
from django.core.validators import MinLengthValidator
# Create your models here.


class SiteBotMember(models.Model):
    customer_id = models.BigIntegerField(primary_key=True)
    chat_id = models.BigIntegerField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, unique=True, max_length=11, validators=[MinLengthValidator(11)])


    def __str__(self):
        return f"{self.phone_number}"


class ProductPlan(models.Model):
    product_id = models.BigIntegerField()
    product_name = models.CharField(max_length=500)
    owner = models.ForeignKey(SiteBotMember, on_delete=models.CASCADE, related_name='orders')
    plan = models.CharField(max_length=50)
    created_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return self.plan

    
    
    