from django.contrib import admin
from .models import PhoneNumber, ReceivedMessage


admin.site.register(PhoneNumber)
admin.site.register(ReceivedMessage)
