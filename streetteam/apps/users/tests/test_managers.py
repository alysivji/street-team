from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import pytest


@pytest.mark.django_db
def test_create_user__happy_path():
    User = get_user_model()
    user = User.objects.create_user(email="normal@user.com", password="foo")
    assert user.email == "normal@user.com"
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user__missing_fields():
    User = get_user_model()
    with pytest.raises(TypeError):
        User.objects.create_user()
    with pytest.raises(TypeError):
        User.objects.create_user(email="")


@pytest.mark.django_db
def test_create_user_requires_valid_email_address():
    User = get_user_model()

    with pytest.raises(ValidationError):
        User.objects.create_user(email="", password="foo")


@pytest.mark.django_db
def test_create_superuser__happy_path():
    User = get_user_model()
    admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
    assert admin_user.email == "super@user.com"
    assert admin_user.is_active is True
    assert admin_user.is_staff is True
    assert admin_user.is_superuser is True


@pytest.mark.django_db
def test_create_superuser__must_set_issuperuser_to_true():
    User = get_user_model()

    with pytest.raises(ValueError):
        User.objects.create_superuser(email="super@user.com", password="foo", is_superuser=False)
