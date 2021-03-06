from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from twilio.twiml.messaging_response import MessagingResponse

from apps.twilio_integration.decorators import validate_twilio_request
from apps.twilio_integration.models import PhoneNumber, ReceivedMessage
from apps.mediahub.models import MediaResource

RECEIVED_SMS = (
    "Something went wrong. "
    "You may have forgotten to attach a picture. "
    "Remember, you can attach up to 5 pictures per message."
)


class TwilioWebhook(APIView):
    @method_decorator(validate_twilio_request(settings.TWILIO_AUTH_TOKEN))
    def post(self, request, format=None):
        data = request.data
        resp = MessagingResponse()

        from_number = data.get("From", None)
        msg_id = data.get("MessageSid", None)

        if not from_number:
            return HttpResponse()
        if not msg_id:
            return HttpResponse()

        from_number, _ = PhoneNumber.objects.get_or_create(number=from_number)
        params = {"twilio_message_id": msg_id, "data": data, "phone_number": from_number}
        msg = ReceivedMessage(**params)
        msg.save()

        if msg_id.startswith("SM"):
            resp.message(body=RECEIVED_SMS)
            return HttpResponse(resp.to_xml(), content_type="application/xml")

        num_media_items = int(data.get("NumMedia", 0))
        media_resources = []
        for num in range(num_media_items):
            content_type = data.get(f"MediaContentType{num}")
            url = data.get(f"MediaUrl{num}")
            item = MediaResource(resource_url=url, content_type=content_type, phone_number=from_number)
            media_resources.append(item)

        MediaResource.objects.bulk_create(media_resources)
        resp.message(body=f"Received {num_media_items} picture(s)! Thank you!")
        return HttpResponse(resp.to_xml(), content_type="application/xml")
