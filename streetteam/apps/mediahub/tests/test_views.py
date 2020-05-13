from io import BytesIO

import pytest

from .factories import UploadedImageFactory


@pytest.mark.django_db
@pytest.mark.end2end
def test_upload_image(client, login_user):
    img = UploadedImageFactory.build(image__width=710, image__height=710)
    image = BytesIO(img.image.read())
    image.name = "test"

    login_user()
    resp = client.post("/images/upload/", {"image": [image]})

    assert resp.status_code == 200
    result = resp.json()
    assert result["num_processed"] == 1
    assert result["num_processed"] == 0
