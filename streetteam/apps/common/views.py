from rest_framework.views import APIView
from django.http import HttpResponse


class DebugEndpoint(APIView):
    def get(self, request, format=None):
        return HttpResponse()

    def post(self, request, format=None):
        return HttpResponse()
