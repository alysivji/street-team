from unittest import mock


class FakeTwilioClient:
    def __init__(self, *, token_sent=None, valid_token=None):
        self.mock = mock.MagicMock()
        self.token_sent = token_sent
        self.valid_token = valid_token

    def __repr__(self):
        return "<FakeTwilioClient>"

    def send_verification_token(self, *args, **kwargs):
        self.mock = mock.MagicMock()
        return self.token_sent

    def valid_verification_token(self, *args, **kwargs):
        self.mock = mock.MagicMock()
        return self.valid_token
