from django.urls import path
from .views import TwilioWebhook

urlpatterns = [path("twilio/", view=TwilioWebhook.as_view())]
