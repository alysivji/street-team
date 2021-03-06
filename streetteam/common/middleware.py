import sys
import uuid

from django.views.debug import technical_500_response


class SuperuserCanViewDebugToolbarInProductionMiddleware:
    """Allow signed-in superuser to view Debug Toolbar

    Trick I found in Two Scoops of Django
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())


class RequestUuidMiddleware:
    """Add uuid to each request"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())
        request.request_id = request_id
        response = self.get_response(request)
        return response
