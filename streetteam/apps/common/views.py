from rest_framework.views import APIView
from django.http import HttpResponse


class DebugEndpoint(APIView):
    def get(self, request, format=None):
        print(request.build_absolute_uri())
        return HttpResponse()

    # @method_decorator(validate_twilio_request(settings.TWILIO_AUTH_TOKEN))
    def post(self, request, format=None):
        print(request.build_absolute_uri())
        print(request.META)
        return HttpResponse()
