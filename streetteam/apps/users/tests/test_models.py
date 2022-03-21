import uuid
from django.contrib.auth import get_user_model
import pytest


@pytest.mark.django_db
def test_user_has_uuid_field():
    User = get_user_model()
    user = User.objects.create_user(email="super@user.com", password="foo")

    assert isinstance(user.id, uuid.UUID)
