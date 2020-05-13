import pytest

from .factories import MediaResourceFactory, UploadedImageFactory
from ..models import MediaResource


@pytest.mark.django_db
def test_create_and_retrieve_message():
    resource = MediaResourceFactory()

    record = MediaResource.objects.first()

    assert record.resource_url == resource.resource_url
    assert record.phone_number.number == resource.phone_number.number


@pytest.mark.django_db
@pytest.mark.current
def test_uploaded_image__user_uploads_image():
    resource = UploadedImageFactory()

    import pdb

    pdb.set_trace()

    record = MediaResource.objects.first()

    assert record.resource_url == resource.resource_url
    assert record.phone_number.number == resource.phone_number.number
