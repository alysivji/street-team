from rest_framework.views import APIView
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse


class TwilioWebhook(APIView):

    # TODO what is format? why is it needed?
    def post(self, request, format=None):
        data = request.data
        resp = MessagingResponse()

        phone_number = data["From"]
        message_id = data["MessageSid"]

        # get or create a phone number
        # create a message

        # handle message
        if message_id.startswith("SM"):
            resp.message(body="Something went wrong. Did you forget an attachment?")
            return HttpResponse(resp.to_xml(), content_type="application/xml")

        return HttpResponse(resp.to_xml(), content_type="application/xml")
