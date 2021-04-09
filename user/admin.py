from django.contrib import admin
from .models import UserBot
# Register your models here.

@admin.register(UserBot)
class UserAdminO(admin.ModelAdmin):
    pass
