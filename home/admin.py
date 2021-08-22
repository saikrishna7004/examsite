from django.contrib import admin
from django.db import transaction

# Register your models here.

from .models import UserVerifyData

class UserVerifyDataAdmin(admin.ModelAdmin):
    fieldsets = [
        ('UserVerifyData Description', {'fields': ['username', 'verified', 'otp']}),
    ]
    list_display = ('username', 'verified', 'otp')
    list_filter = ['username']
    search_fields = ['verified', 'username']

admin.site.register(UserVerifyData, UserVerifyDataAdmin)
