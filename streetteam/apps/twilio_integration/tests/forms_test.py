import pytest

from .utils import FakeTwilioClient
from apps.twilio_integration.adapter import PhoneNumberDTO
from apps.twilio_integration.forms import ConfirmVerificationCodeForm, LinkPhoneNumberForm
from apps.twilio_integration.exceptions import PhoneNumberNotValid

MODULE_TO_TEST = "apps.twilio_integration.forms"


@pytest.fixture
def PatchedTwilio(patcher):
    def _wrapper(valid_number=None):
        obj = FakeTwilioClient(valid_number=valid_number)
        return patcher(MODULE_TO_TEST, namespace="twilio", replacement=obj)

    return _wrapper


@pytest.mark.unit
def test_phone_number_form__valid_input(PatchedTwilio):
    # Arrange
    return_value = PhoneNumberDTO(number="+13125555555", country_code="US")
    PatchedTwilio(valid_number=return_value)
    form_data = {"phone_number": "312 555 5555"}

    form = LinkPhoneNumberForm(data=form_data)

    assert form.is_valid()


@pytest.mark.unit
def test_phone_number_form__invalid_input__regex_fail():
    form_data = {"phone_number": "not_valid_number"}
    form = LinkPhoneNumberForm(data=form_data)
    assert not form.is_valid()


@pytest.mark.unit
def test_phone_number_form__invalid_input__non_usa_phone_number(PatchedTwilio):
    # Arrange
    PatchedTwilio(valid_number=PhoneNumberNotValid())
    form_data = {"phone_number": "416 555 5555"}

    form = LinkPhoneNumberForm(data=form_data)

    assert not form.is_valid()


@pytest.mark.unit
def test_confirmation_verification_code_form__valid_input():
    form = ConfirmVerificationCodeForm(data={"code": "test_code"})
    assert form.is_valid()
