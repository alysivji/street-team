from django.urls import path
from .views import enter_phone_number_to_send_verification_code, verify_code_send_via_sms, success, TwilioWebhook

urlpatterns = [
    path("twilio/integration", view=TwilioWebhook.as_view()),  # TODO change in twilio console
    path(
        "confirm_phone_number/",
        view=enter_phone_number_to_send_verification_code,
        name="enter_phone_number_to_send_verification_code",
    ),
    path("enter_verification_code/", view=verify_code_send_via_sms, name="verify_code_send_via_sms"),
    path("sucess/", view=success, name="success"),
]
