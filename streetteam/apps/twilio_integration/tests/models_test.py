import pytest

from .factories import PhoneNumberFactory, ReceivedMessageFactory
from .utils import FakeTwilioClient
from apps.twilio_integration.models import PhoneNumber, ReceivedMessage
from apps.users.tests.factories import UserFactory

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
    phone_number = PhoneNumberFactory()
    record = PhoneNumber.objects.first()
    assert record.number == phone_number.number


@pytest.mark.unit
@pytest.mark.state_machine
@pytest.mark.django_db
def test_state_transition__link_acount__happy_path(PatchedTwilio):
    # Arrange
    phone_number = PhoneNumberFactory(user=None)
    user = UserFactory()
    PatchedTwilio()

    # Act
    assert phone_number.account_link_state == PhoneNumber.AccountLinkState.INITIAL_STATE
    phone_number.link_account(user)

    # Assert
    assert phone_number.account_link_state == PhoneNumber.AccountLinkState.ATTEMPT_PHONE_LINK


#################
# ReceivedMessage
#################
@pytest.mark.django_db
def test_create_and_retrieve_message():
    # Arrange
    random_data = {"field": "value"}
    received_message = ReceivedMessageFactory(data=random_data)

    # Act
    record = ReceivedMessage.objects.first()

    # Assert
    assert record.data == random_data
    assert record.phone_number.number == received_message.phone_number.number
