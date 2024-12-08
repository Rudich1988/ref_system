from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'phone_number',
        'is_active',
        'invite_code',
        'created_at',
    ]
    search_fields = ['phone_number', 'invite_code']