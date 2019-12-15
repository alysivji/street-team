from unittest import mock


class FakeTwilioClient:
    def __init__(self, *, valid_number=None, token_sent=None, valid_token=None):
        self.mock = mock.MagicMock()
        self.valid_number = valid_number
        self.token_sent = token_sent
        self.valid_token = valid_token

    def __repr__(self):
        return "<FakeTwilioClient>"

    def verify_phone_number(self, *args, **kwargs):
        self.mock = mock.MagicMock()

        if isinstance(self.valid_number, Exception):
            raise self.valid_number

        return self.valid_number

    def send_verification_token(self, *args, **kwargs):
        self.mock = mock.MagicMock()
        return self.token_sent

    def valid_verification_token(self, *args, **kwargs):
        self.mock = mock.MagicMock()
        return self.valid_token
