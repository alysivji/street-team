import json
import pytest


@pytest.mark.django_db
def test_send_SMS__receive_forget_attachment_message(client):
    # Arrange
    filepath = "streetteam/apps/twilio_integration/tests/files/twilio_webhook__send_sms.json"
    with open(filepath, "r") as read_file:
        data = json.load(read_file)

    # Act
    resp = client.post("/integration/twilio/", data=data)

    # Assert
    assert b"Something went wrong" in resp.getvalue()
