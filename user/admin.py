from django.contrib import admin
from .models import SiteBotMember
# Register your models here.


@admin.register(SiteBotMember)
class SiteBotAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'chat_id', 'phone_number']
