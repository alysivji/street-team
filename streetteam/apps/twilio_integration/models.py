from django.contrib.postgres.fields import JSONField
from django.db import models
from django_fsm import FSMField, transition

from apps.common.models import BaseModel
from apps.users.models import User


class PhoneNumber(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=30, unique=True)

    user = models.ForeignKey(User, related_name="phone_numbers", on_delete=models.CASCADE)

    class AccountLinkState:
        """Has phone_number been linked to account"""

        UNLINKED_PHONE_NUMBER = "unlinked_phone_number"
        ATTEMPT_PHONE_LINK = "attempt_phone_link"
        PHONE_LINK_SUCCESS = "phone_link_success"
        PHONE_LINK_FAILED = "phone_link_failed"

        CHOICES = [
            (UNLINKED_PHONE_NUMBER,) * 2,
            (ATTEMPT_PHONE_LINK,) * 2,
            (PHONE_LINK_SUCCESS,) * 2,
            (PHONE_LINK_FAILED,) * 2,
        ]

        INITIAL_STATE = UNLINKED_PHONE_NUMBER

    account_link_state = FSMField(
        default=AccountLinkState.INITIAL_STATE, choices=AccountLinkState.CHOICES, protected=True
    )

    # TODO save should also have a transition
    # override SAVE ala 2 scoops

    @transition(
        field=account_link_state,
        source=AccountLinkState.UNLINKED_PHONE_NUMBER,
        target=AccountLinkState.ATTEMPT_PHONE_LINK,
    )
    def link_phone_number(self):
        # ask them to enter a phone number, use Twilio API to ensure number is valid
        # send a text message to that number with code, store code in database
        pass

    # @transition(
    #     field=AccountLinkState, source=AccountLinkState.ATTEMPT_PHONE_LINK,
    # target=AccountLinkState.PHONE_LINK_SUCCESS,
    # on_error=AccountLinkState.PHONE_LINK_FAILED
    # )
    # def phone_successfully_linked(self, entered_code):
    #     pass

    # @transition(field=AccountLinkState, source=AccountLinkState.PHONE_LINK_FAILED,
    # target=AccountLinkState.ATTEMPT_PHONE_LINK)
    # def retry_link_phone_number(self):
    #     pass


class ReceivedMessage(BaseModel):
    id = models.AutoField(primary_key=True)
    twilio_message_id = models.CharField(max_length=34)
    data = JSONField()

    phone_number = models.ForeignKey(PhoneNumber, related_name="messages", on_delete=models.CASCADE)
