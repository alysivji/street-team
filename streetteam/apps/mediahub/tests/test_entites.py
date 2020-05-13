import pytest

from ..entities import MediaPost, EVENTS_LIST
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
    # TODO put this into the manager
    uploaded_image = UploadedImage.objects.first()
    events = [event.to_dict() for event in uploaded_image.events.order_by("id").all()]

    all_events = []
    for event in events:
        for EventClass in EVENTS_LIST:
            if EventClass.match(event):
                all_events.append(EventClass(**event["details"]))

    post = MediaPost(all_events)

    assert post.caption == "final caption"
