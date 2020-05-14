import pytest

from .factories import (
    AddCaptionEventFactory,
    CropImageEventFactory,
    MediaResourceFactory,
    ModifyCaptionEventFactory,
    RejectPostEventFactory,
    SubmitPostEventFactory,
    UploadedImageFactory,
)
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
def test_create_and_retrieve_upload_image_event():
    uploaded_image = UploadedImageFactory(image__width=710, image__height=710)

    record = PostEvent.objects.first()

    assert record.name == "upload_image"
    assert record.performed_by == uploaded_image.uploaded_by
    assert record.image.image.width == 710
    assert record.image.image.height == 710


@pytest.mark.django_db
def test_create_and_retrieve_crop_image_event():
    uploaded_image = UploadedImageFactory(image__width=100, image__height=100)
    event = CropImageEventFactory(image=uploaded_image, data={"top": 0, "left": 0, "bottom": 50, "right": 50})

    record = PostEvent.objects.last()

    assert record.name == event.name
    assert record.data == event.data
    assert record.performed_by == event.performed_by


@pytest.mark.django_db
def test_create_and_retrieve_add_caption_event():
    event = AddCaptionEventFactory(data={"caption": "test caption"})

    record = PostEvent.objects.last()

    assert record.name == event.name
    assert record.data == event.data
    assert record.performed_by == event.performed_by


@pytest.mark.django_db
def test_create_and_retrieve_modify_caption_event():
    event = ModifyCaptionEventFactory(data={"caption": "new caption"})

    record = PostEvent.objects.last()

    assert record.name == event.name
    assert record.data == event.data
    assert record.performed_by == event.performed_by


@pytest.mark.django_db
def test_create_and_retrieve_submit_event():
    event = SubmitPostEventFactory(data={})

    record = PostEvent.objects.last()

    assert record.name == event.name
    assert record.data == event.data
    assert record.performed_by == event.performed_by


@pytest.mark.django_db
def test_create_and_retrieve_reject_post_event():
    event = RejectPostEventFactory(data={"reason": "Used similar picture"})

    record = PostEvent.objects.last()

    assert record.name == event.name
    assert record.data == event.data
    assert record.performed_by == event.performed_by
