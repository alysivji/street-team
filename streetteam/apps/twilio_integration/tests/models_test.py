import pytest

from .utils import FakeTwilioClient
from apps.twilio_integration.models import PhoneNumber, ReceivedMessage
from apps.users.models import User

MODULE_TO_TEST = "apps.twilio_integration.models"


@pytest.fixture
def PatchedTwilio(patcher):
    def _wrapper(token_sent=None):
        obj = FakeTwilioClient(token_sent=token_sent)
        return patcher(MODULE_TO_TEST, namespace="twilio", replacement=obj)

    return _wrapper


#############
# PhoneNumber
#############
@pytest.mark.unit
@pytest.mark.django_db
def test_create_and_retrieve_phone_number():
    phone_number = PhoneNumber(number="+13125551234")
    phone_number.save()

    record = PhoneNumber.objects.get(number="+13125551234")
    assert record.number == "+13125551234"


# TODO thinking out loud
# unit testing this for happy path only is a bit ridiculous
# we should be testing for all cases to ensure flow is proper
# view tests should test happy
@pytest.mark.unit
@pytest.mark.state_machine
@pytest.mark.django_db
def test_state_transition__link_acount__happy_path(PatchedTwilio):
    # Arrange
    # create phone number and initial state
    phone_number = PhoneNumber(number="+13125551234")
    phone_number.save()
    assert phone_number.account_link_state == PhoneNumber.AccountLinkState.INITIAL_STATE
    # create user
    user = User(email="test@user.com")
    user.save()
    PatchedTwilio()

    # Act
    phone_number.link_account(user)

    # Assert
    phone_number.account_link_state == PhoneNumber.AccountLinkState.ATTEMPT_PHONE_LINK


#################
# ReceivedMessage
#################
@pytest.mark.django_db
def test_create_and_retrieve_message():
    phone_number = PhoneNumber(number="+13125551234")
    phone_number.save()

    random_data = {"field": "value"}
    received_message = ReceivedMessage(data=random_data, phone_number=phone_number)
    received_message.save()

    record = ReceivedMessage.objects.first()
    assert record.data == random_data
    assert record.phone_number.number == "+13125551234"
