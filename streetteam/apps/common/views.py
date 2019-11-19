from django.http import HttpResponse
from django.views.generic.base import TemplateView
from rest_framework.views import APIView


class DebugEndpoint(APIView):
    def get(self, request, format=None):
        return HttpResponse()

    def post(self, request, format=None):
        return HttpResponse()


class DebugPageView(TemplateView):

    template_name = "debug.html"
