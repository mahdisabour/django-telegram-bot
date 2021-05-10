from django.contrib import admin
from .models import SiteBotMember, ProductPlan
# Register your models here.


@admin.register(SiteBotMember)
class SiteBotAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'chat_id', 'phone_number']

@admin.register(ProductPlan)
class ProductPlanAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'owner', 'expiration_date', 'product_name', 'plan']
