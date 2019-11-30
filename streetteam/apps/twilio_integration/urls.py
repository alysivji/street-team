from django.urls import path
from .views import TwilioWebhook, get_name, verify_code_send_via_sms, success

urlpatterns = [
    path("twilio/", view=TwilioWebhook.as_view()),  # TODO rename and change in console
    path("confirm_phone_number/", view=get_name),
    path("enter_verification_code/", view=verify_code_send_via_sms, name="verify_code_send_via_sms"),
    path("sucess/", view=success, name="success"),
]
