import pytest

from .factories import MediaResourceFactory, UploadedImageFactory, PostEventFactory, UploadImageEventFactory
from ..models import MediaResource, UploadedImage, PostEvent


@pytest.mark.django_db
def test_create_and_retrieve_message():
    resource = MediaResourceFactory()

    record = MediaResource.objects.first()

    assert record.resource_url == resource.resource_url
    assert record.phone_number.number == resource.phone_number.number


@pytest.mark.django_db
def test_create_and_retrieve_uploaded_image():
    resource = UploadedImageFactory()

    record = UploadedImage.objects.first()

    assert record.image.width == resource.image.width
    assert record.image.height == resource.image.height


@pytest.mark.django_db
def test_create_and_retrieve_post_event_factory():
    event = PostEventFactory()

    record = PostEvent.objects.first()

    assert record.name == event.name
    assert record.data == event.data
    assert record.performed_by == event.performed_by


@pytest.mark.django_db
def test_create_and_retrieve_upload_image_event():
    uploaded_image = UploadedImageFactory(image__width=710, image__height=710)
    event = UploadImageEventFactory(image=uploaded_image)

    record = PostEvent.objects.first()

    assert record.name == event.name
    assert record.data == event.data
    assert record.performed_by == event.performed_by
    assert record.image.image.width == 710
    assert record.image.image.height == 710
