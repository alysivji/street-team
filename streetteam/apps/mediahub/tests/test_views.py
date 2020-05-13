from io import BytesIO

import pytest

from .factories import UploadedImageFactory
from ..models import PostEvent


@pytest.mark.django_db
@pytest.mark.end2end
@pytest.mark.current
def test_upload_image(client, login_user):
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
