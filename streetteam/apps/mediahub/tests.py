import pytest
from apps.mediahub.models import MediaResource
from apps.twilio_integration.models import PhoneNumber


@pytest.mark.django_db
def test_create_and_retrieve_message():
    phone_number = PhoneNumber(number="+13125551234")
    phone_number.save()

    random_url = "https://alysivji.github.io"
    resource = MediaResource(resource_url=random_url, phone_number=phone_number)
    resource.save()

    record = MediaResource.objects.first()
    assert record.resource_url == random_url
    assert record.phone_number.number == "+13125551234"
