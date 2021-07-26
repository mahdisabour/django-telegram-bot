from django.contrib import admin
from .models import SiteBotMember, ProductPlan, Message, Group
# Register your models here.


@admin.register(SiteBotMember)
class SiteBotAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'chat_id', 'phone_number', "group"]
    list_filter = ['group']

@admin.register(ProductPlan)
class ProductPlanAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'owner', 'expiration_date', 'product_name', 'plan']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'timing']
    filter_horizontal = ['receivers']



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name',]