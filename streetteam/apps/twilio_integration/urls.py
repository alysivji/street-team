from django.urls import path
from .views import TwilioWebhook, get_name

urlpatterns = [
    path("twilio/", view=TwilioWebhook.as_view()),  # TODO rename and change in console
    path("confirm_phone_number/", view=get_name),
]
