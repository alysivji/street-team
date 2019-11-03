import json
import pytest


@pytest.mark.django_db
def test_send_SMS__receive_error_message(client):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__send_sms.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)

    # Act
    resp = client.post("/integration/twilio/", data=data)

    # Assert
    assert b"Something went wrong" in resp.getvalue()


@pytest.mark.django_db
def test_send_1_picture_MMS__receive_thank_you_message(client):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_1_picture.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)

    # Act
    resp = client.post("/integration/twilio/", data=data)

    # Assert
    assert b"Received 1 picture(s)! Thank you!" in resp.getvalue()


@pytest.mark.django_db
def test_send_3_picture_MMS__receive_thank_you_message(client):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_3_pictures.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)

    # Act
    resp = client.post("/integration/twilio/", data=data)

    # Assert
    assert b"Received 3 picture(s)! Thank you!" in resp.getvalue()


@pytest.mark.django_db
def test_send_5_picture_MMS__receive_thank_you_message(client):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_5_pictures.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)

    # Act
    resp = client.post("/integration/twilio/", data=data)

    # Assert
    assert b"Received 5 picture(s)! Thank you!" in resp.getvalue()


@pytest.mark.django_db
def test_send_6_picture_MMS__receive_error_message(client):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__attach_6_pictures.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)

    # Act
    resp = client.post("/integration/twilio/", data=data)

    # Assert
    assert b"Something went wrong" in resp.getvalue()
