from io import BytesIO

import pytest

from .factories import UploadedImageFactory
from ..models import PostEvent


@pytest.mark.django_db
@pytest.mark.end2end
@pytest.mark.xfail
def test_upload_image(client, login_user):
    # TODO need to associate with event
    img = UploadedImageFactory.build(image__width=710, image__height=710)
    image = BytesIO(img.image.read())
    image.name = "test"

    login_user()
    resp = client.post("/images/upload/", {"image": [image]})

    assert resp.status_code == 200
    result = resp.json()
    assert result["num_processed"] == 1
    assert result["num_not_valid"] == 0

    events = PostEvent.objects.all()
    assert len(events) == 1
    assert events[0].name == "upload_image"


@pytest.mark.django_db
@pytest.mark.end2end
def test_crop_image(client, login_user):
    image = UploadedImageFactory(image__width=710, image__height=710)

    login_user(image.uploaded_by)
    data = {"cropLeft": 100, "cropTop": 100, "cropWidth": 100, "cropHeight": 100}
    resp = client.post(f"/images/{image.uuid}/crop", data=data)

    assert resp.status_code == 200

    events = PostEvent.objects.all()
    assert len(events) == 2
    crop_event = events[1]
    assert crop_event.name == "crop_image"
    assert crop_event.data == {"left": 100, "top": 100, "bottom": 200, "right": 200}
