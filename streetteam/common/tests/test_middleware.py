import pytest


class TestRequestUuidMiddleware:
    def test_request_has_uuid(self, client):
        response = client.get("/healthcheck")
        request = response.wsgi_request
        assert getattr(request, "request_uuid") is not None

    def test_request_does_not_have_guid_field(self, client):
        response = client.get("/healthcheck")
        request = response.wsgi_request
        with pytest.raises(AttributeError):
            getattr(request, "request_guid")
