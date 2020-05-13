import pytest

from ..entities import MediaPost
from ..models import UploadedImage
from .factories import AddCaptionEventFactory, ModifyCaptionEventFactory, UploadedImageFactory


@pytest.mark.django_db
@pytest.mark.current
def test_caption_reducer():
    # create events for image
    image = UploadedImageFactory()
    AddCaptionEventFactory(image=image, data={"caption": "test caption"})
    ModifyCaptionEventFactory(image=image, data={"caption": "new caption"})
    ModifyCaptionEventFactory(image=image, data={"caption": "final caption"})

    # Action
    uploaded_image = UploadedImage.objects.first()
    events = uploaded_image.events.get_log()
    post = MediaPost(events)

    assert post.caption == "final caption"
