from django.contrib import admin
from .models import UserBot, VipMembers, SiteBotMember
# Register your models here.

@admin.register(UserBot)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(VipMembers)
class VipMemberAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_number', 'telegram_id']


@admin.register(SiteBotMember)
class SiteBotAdmin(admin.ModelAdmin):
    list_display = ['customer_id', 'chat_id', 'phone_number']
