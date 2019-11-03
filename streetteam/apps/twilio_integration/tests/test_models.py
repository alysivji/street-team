import pytest
from apps.twilio_integration.models import PhoneNumber, ReceivedMessage


@pytest.mark.django_db
def test_create_and_retrieve_phone_number():
    phone_number = PhoneNumber(number="+13125551234")
    phone_number.save()

    record = PhoneNumber.objects.get(number="+13125551234")
    assert record.number == "+13125551234"


@pytest.mark.django_db
def test_create_and_retrieve_message():
    phone_number = PhoneNumber(number="+13125551234")
    phone_number.save()

    random_data = {"field": "value"}
    received_message = ReceivedMessage(data=random_data, phone_number=phone_number)
    received_message.save()

    record = ReceivedMessage.objects.first()
    assert record.data == random_data
    assert record.phone_number.number == "+13125551234"
