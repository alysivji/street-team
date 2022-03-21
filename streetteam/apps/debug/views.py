from django.http import HttpResponse
from django.views.generic.base import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class DebugEndpoint(APIView):
    def get(self, request, format=None):
        raise ValueError

    def post(self, request, format=None):
        return HttpResponse()


class AuthenticatedDebugEndpoint(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class DebugPageView(TemplateView):

    template_name = "debug.html"
