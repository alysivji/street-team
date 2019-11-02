import json

from rest_framework.views import APIView
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse

count = 0


class DebugView(APIView):

    def post(self, request, format=None):
        data = request.data
        print(data)

        global count
        count += 1

        import pdb; pdb.set_trace()

        with open(f"{count}.json", "w") as f:
            json.dump(data, f)

        resp = MessagingResponse()
        return HttpResponse(resp.to_xml(), content_type="application/xml")
