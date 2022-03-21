import pytest

from .factories import UserFactory


@pytest.mark.django_db
class TestCreateNewUser:
    def test_create_user_happy_path(self, client):
        user_details = {"email": "test@user.com", "password": "ValidPassword1"}

        response = client.post("/users/", data=user_details, format="json")

        assert response.status_code == 201

    def test_create_user__email_already_registered(self, client):
        UserFactory(email="already@registered.com")
        user_details = {"email": "already@registered.com", "password": "ValidPassword1"}

        response = client.post("/users/", data=user_details, format="json")

        assert response.status_code == 400
