import uuid
from django.contrib.auth import get_user_model
import pytest


@pytest.mark.django_db
def test_user_has_uuid_field():
    User = get_user_model()
    user = User.objects.create_user("super@user.com", "foo")

    assert isinstance(user.uuid, uuid.UUID)
