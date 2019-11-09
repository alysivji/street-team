from django.conf import settings
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from django.http import HttpResponse

from apps.twilio_integration.decorators import validate_twilio_request


class DebugEndpoint(APIView):
    def get(self, request, format=None):
        print(request.build_absolute_uri())
        return HttpResponse()

    @method_decorator(validate_twilio_request(settings.TWILIO_AUTH_TOKEN))
    def post(self, request, format=None):
        print(request.build_absolute_uri())
        print(request.META)
        return HttpResponse()
