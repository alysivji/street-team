import pytest

from .factories import AddCaptionEventFactory, ModifyCaptionEventFactory, UploadedImageFactory
from ..entities import MediaPost
from ..models import UploadedImage


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

    # TODO add this to manager
    events = [
        dict([("details", event.data), ("type", event.name)]) for event in uploaded_image.events.order_by("id").all()
    ]
    post = MediaPost(events)

    assert post.caption == "final caption"
