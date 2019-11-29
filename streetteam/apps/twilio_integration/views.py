from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from twilio.twiml.messaging_response import MessagingResponse

from .decorators import validate_twilio_request
from .forms import ReceiverForm
from .models import PhoneNumber, ReceivedMessage
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


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = ReceiverForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # return HttpResponseRedirect('/thanks/')

            # confirm number is valid using

            return HttpResponse({"ping": "pong"}, content_type="application/json")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ReceiverForm()

    return render(request, "phone_number.html", {"form": form})
