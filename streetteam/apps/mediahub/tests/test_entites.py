import pytest

from ..entities import MediaPost
from ..models import UploadedImage
from .factories import (
    AddCaptionEventFactory,
    CropImageEventFactory,
    ModifyCaptionEventFactory,
    UploadedImageFactory,
    UploadImageEventFactory,
)


@pytest.mark.django_db
def test_caption_reducer():
    # Arrange
    image = UploadedImageFactory()
    AddCaptionEventFactory(image=image, data={"caption": "test caption"})
    ModifyCaptionEventFactory(image=image, data={"caption": "new caption"})
    ModifyCaptionEventFactory(image=image, data={"caption": "final caption"})

    # Act
    uploaded_image = UploadedImage.objects.first()
    events = uploaded_image.events.get_log()
    post = MediaPost(events)

    # Assert
    assert post.caption == "final caption"


@pytest.mark.django_db
@pytest.mark.current
def test_upload_image_and_crop_reducer():
    # Arrange
    image = UploadedImageFactory(image__width=100, image__height=100)
    UploadImageEventFactory(image=image)
    expected_cropbox = {"top": 0, "left": 0, "bottom": 50, "right": 50}
    CropImageEventFactory(image=image, data=expected_cropbox)

    # Act
    uploaded_image = UploadedImage.objects.first()
    events = uploaded_image.events.get_log()
    post = MediaPost(events)

    # Assert
    assert post.cropbox._asdict() == expected_cropbox
