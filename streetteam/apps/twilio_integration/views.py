from rest_framework.views import APIView
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse


class TwilioWebhook(APIView):

    # TODO what is format? why is it needed?
    def post(self, request, format=None):
        data = request.data
        print(data)

        resp = MessagingResponse()
        return HttpResponse(resp.to_xml(), content_type="application/xml")
