from typing import NamedTuple
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client


class PhoneNumber(NamedTuple):
    is_valid: bool
    phone_number: str  # E.164 format


class TwilioAdapter:
    def __init__(self, account_sid, auth_token, service_sid=None):
        self.client = Client(account_sid, auth_token)
        self.service_sid = service_sid

    def __repr__(self):
        return "<TwilioAdapter>"

    def verify_phone_number(self, phone_number):
        try:
            resp = self.client.lookups.phone_numbers(phone_number).fetch()
        except TwilioRestException:  # invalid number returns 404
            return PhoneNumber(False, "")

        if resp.country_code not in ["US"]:
            return PhoneNumber(False, "")

        return PhoneNumber(True, resp.phone_number)

    def send_verification_token(self, phone_number):
        verification = self.client.verify.services(self.service_sid).verifications.create(
            to=phone_number, channel="sms"
        )
        # what happens when we put in a bad phone number?
        return verification

    def validate_verification_token(self, phone_number, verification_token):
        verification = self.client.verify.services(self.service_sid).verification_checks.create(
            to=phone_number, code=verification_token
        )
        if not verification.valid:
            raise ValueError  # TODO custom error
        return verification


if __name__ == "__main__":
    import os  # noqa

    twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_service_sid = os.getenv("TWILIO_SERVICE_SID")

    twilio = TwilioAdapter(twilio_account_sid, twilio_auth_token, twilio_service_sid)
