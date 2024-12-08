from django.contrib import admin

from .models import InviteCode


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'code']
    search_fields = ['id', 'code']
