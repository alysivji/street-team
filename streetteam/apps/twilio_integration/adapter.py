# TODO log everything going in and coming back from twilio...
# easier to debug
# TODO catch twilio exceptions and log them

from typing import NamedTuple
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


class PhoneNumber(NamedTuple):
    is_valid: bool
    number: str  # E.164 format
    country_code: str


class PhoneNumberVerificationResponse(NamedTuple):
    pass


class VerificationCodeReponse(NamedTuple):
    is_valid: bool


class TwilioAdapter:
    def __init__(self, account_sid, auth_token, service_sid=None):
        self.client = Client(account_sid, auth_token)
        self.service_sid = service_sid

    def __repr__(self):
        return "<TwilioAdapter>"

    def verify_phone_number(self, phone_number: str) -> PhoneNumber:
        try:
            resp = self.client.lookups.phone_numbers(phone_number).fetch()
        except TwilioRestException:  # invalid number returns 404
            return PhoneNumber(is_valid=False, number="", country_code="")

        return PhoneNumber(is_valid=True, number=resp.phone_number, country_code=resp.country_code)

    def send_verification_token(self, phone_number: str):
        try:
            self.client.verify.services(self.service_sid).verifications.create(to=phone_number, channel="sms")
        except TwilioRestException:
            return False

        return True

    def valid_verification_token(self, phone_number: str, verification_token: str):
        verification = self.client.verify.services(self.service_sid).verification_checks.create(
            to=phone_number, code=verification_token
        )
        if not verification.valid:
            return False
        return True


if __name__ == "__main__":
    import os  # noqa

    twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_service_sid = os.getenv("TWILIO_SERVICE_SID")

    twilio = TwilioAdapter(twilio_account_sid, twilio_auth_token, twilio_service_sid)
else:
    from django.conf import settings  # noqa

    twilio = TwilioAdapter(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_SERVICE_SID)
