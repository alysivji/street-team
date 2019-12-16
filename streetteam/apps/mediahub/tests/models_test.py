import pytest

from .factories import MediaResourceFactory
from apps.mediahub.models import MediaResource


@pytest.mark.django_db
def test_create_and_retrieve_message():
    resource = MediaResourceFactory()

    record = MediaResource.objects.first()

    assert record.resource_url == resource.resource_url
    assert record.phone_number.number == resource.phone_number.number
