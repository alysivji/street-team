from django.urls import path
from .views import TwilioWebhook

urlpatterns = [path("twilio/", view=TwilioWebhook.as_view())]  # TODO rename and change in console
