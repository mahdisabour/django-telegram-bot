from django.contrib import admin
from .models import UserBot, VipMembers
# Register your models here.

@admin.register(UserBot)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(VipMembers)
class VipMemberAdmin(admin.ModelAdmin):
    pass
