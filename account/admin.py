from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Balance)
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone']
    list_display_links = ['username', 'phone']


