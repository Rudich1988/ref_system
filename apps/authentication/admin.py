from django.contrib import admin

from .models import PhoneAuth


@admin.register(PhoneAuth)
class PhoneAuthAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'phone_number',
        'code',
        'created_at',
        'expires_at'
    ]
    search_fields = ['phone_number']
