import pytest


@pytest.mark.django_db
def test_new_user_can_perform_jwt_authentication(client):
    # Step 1: Create New User
    email = "test@user.com"
    password = "ValidPassword1"
    login_details = {"email": email, "password": password}
    response = client.post("/users/", data=login_details, format="json")
    assert response.status_code == 201

    # Step 2: Obtain Access Token
    response = client.post("/users/token/", data=login_details, format="json")
    assert response.status_code == 200

    response_json = response.json()
    access_token = response_json["access"]
    assert access_token
    refresh_token = response_json["refresh"]
    assert refresh_token

    # Step 3: Access Authenticated Endpoint with Access Token
    response = client.get("/debug/authenticated/", HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == 200
