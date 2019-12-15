import pytest

from ..utils import FakeTwilioClient
from ...adapter import PhoneNumberDTO
from ...models import PhoneNumber


@pytest.fixture
def PatchedTwilio(patcher):
    def _wrapper(module_to_patch, valid_number=None, token_sent=None, valid_token=None):
        obj = FakeTwilioClient(valid_number=valid_number, token_sent=token_sent, valid_token=valid_token)
        return patcher(module_to_patch, namespace="twilio", replacement=obj)

    return _wrapper


@pytest.mark.wip
@pytest.mark.e2e
@pytest.mark.django_db
def test_connect_phone_number__unlinked_user(client, login_user, PatchedTwilio):
    # Arrange
    number = "+13125555555"
    return_value = return_value = PhoneNumberDTO(number=number, country_code="US")
    PatchedTwilio("apps.twilio_integration.forms", valid_number=return_value)
    PatchedTwilio("apps.twilio_integration.models", token_sent=True, valid_token=True)
    confirm_phone_uri = "http://testserver/sms/confirm_phone_number/"
    verification_uri = "http://testserver/sms/enter_verification_code/"

    # create new user and log them in
    user = login_user()

    # hit the phone confirmation
    resp = client.get(confirm_phone_uri)

    # confirm page is as expected
    assert resp.status_code == 200
    assert b"Your phone number" in resp.content

    # fill out form
    phone_number = "555 555 5555"
    form_data = {"phone_number": phone_number}

    # post form data
    resp = client.post(confirm_phone_uri, data=form_data)

    # assert we have sent a confirmation code
    phone_number = user.phone_numbers.first()
    assert phone_number.number == number
    assert phone_number.account_link_state == PhoneNumber.AccountLinkState.ATTEMPT_PHONE_LINK

    # have user confirm valid code
    resp = client.get(verification_uri)

    # confirm page is as expected
    assert resp.status_code == 200
    assert b"Enter verification code" in resp.content

    # fill out form
    form_data = {"code": "correct_verification_code"}

    # post form data
    resp = client.post(verification_uri, data=form_data)

    # assert we have sent a confirmation code
    phone_number = user.phone_numbers.first()
    assert phone_number.number == number
    assert phone_number.account_link_state == PhoneNumber.AccountLinkState.PHONE_LINK_SUCCESS


@pytest.mark.todo
@pytest.mark.e2e
def test_connect_phone_number__relinked_user():
    pass
