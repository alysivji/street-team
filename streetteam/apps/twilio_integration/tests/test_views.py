import json

from django.conf import settings
import pytest
from twilio.request_validator import RequestValidator


@pytest.fixture
def create_twilio_headers():
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

    def wrapper(uri, data):
        return {"HTTP_X_TWILIO_SIGNATURE": validator.compute_signature(uri, data)}

    return wrapper


@pytest.mark.django_db
def test_send_SMS__receive_error_message(client, create_twilio_headers):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__send_sms.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    uri = "http://testserver/integration/twilio/"
    headers = create_twilio_headers(uri, data)

    # Act
    resp = client.post(uri, data=data, **headers)

    # Assert
    assert b"Something went wrong" in resp.getvalue()


@pytest.mark.django_db
def test_send_1_picture_MMS__receive_thank_you_message(client, create_twilio_headers):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_1_picture.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    uri = "http://testserver/integration/twilio/"
    headers = create_twilio_headers(uri, data)

    # Act
    resp = client.post(uri, data=data, **headers)

    # Assert
    assert b"Received 1 picture(s)! Thank you!" in resp.getvalue()


@pytest.mark.django_db
def test_send_3_picture_MMS__receive_thank_you_message(client, create_twilio_headers):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_3_pictures.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    uri = "http://testserver/integration/twilio/"
    headers = create_twilio_headers(uri, data)

    # Act
    resp = client.post(uri, data=data, **headers)

    # Assert
    assert b"Received 3 picture(s)! Thank you!" in resp.getvalue()


@pytest.mark.django_db
def test_send_5_picture_MMS__receive_thank_you_message(client, create_twilio_headers):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_5_pictures.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    uri = "http://testserver/integration/twilio/"
    headers = create_twilio_headers(uri, data)

    # Act
    resp = client.post(uri, data=data, **headers)

    # Assert
    assert b"Received 5 picture(s)! Thank you!" in resp.getvalue()


@pytest.mark.django_db
def test_send_6_picture_MMS__receive_error_message(client, create_twilio_headers):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_6_pictures.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)
    uri = "http://testserver/integration/twilio/"
    headers = create_twilio_headers(uri, data)

    # Act
    resp = client.post(uri, data=data, **headers)

    # Assert
    assert b"Something went wrong" in resp.getvalue()
