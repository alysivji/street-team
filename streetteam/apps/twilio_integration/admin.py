from django.contrib import admin
from django_fsm_log.admin import StateLogInline

from .models import PhoneNumber, ReceivedMessage


@admin.register(PhoneNumber)
class FSMModelAdmin(admin.ModelAdmin):
    inlines = [StateLogInline]


admin.site.register(ReceivedMessage)
