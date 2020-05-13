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
    events = []
    for event in uploaded_image.events.order_by("id").all():
        for EventClass in EVENTS_LIST:
            my_event = event.to_dict()
            if EventClass.match(my_event):
                events.append(EventClass(**my_event["details"]))

    post = MediaPost(events)

    assert post.caption == "final caption"
