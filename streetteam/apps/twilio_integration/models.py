from django_fsm import FSMField, transition
from django.contrib.postgres.fields import JSONField
from django.db import models

from .adapter import twilio
from apps.common.models import BaseModel
from apps.users.models import User


class PhoneNumber(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=30, unique=True)

    user = models.ForeignKey(User, null=True, related_name="phone_numbers", on_delete=models.CASCADE)

    def __repr__(self):
        return f"<PhoneNumber: {self.number}>"

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

    account_link_state = FSMField(default=AccountLinkState.INITIAL_STATE, choices=AccountLinkState.CHOICES)

    @transition(
        field=account_link_state,
        source=AccountLinkState.UNLINKED_PHONE_NUMBER,
        target=AccountLinkState.ATTEMPT_PHONE_LINK,
    )
    def link_account(self, user):
        self.user = user
        twilio.send_verification_token(self.number)

    @transition(
        field=account_link_state,
        source=AccountLinkState.ATTEMPT_PHONE_LINK,
        target=AccountLinkState.PHONE_LINK_SUCCESS,
        on_error=AccountLinkState.PHONE_LINK_FAILED,
    )
    def confirm_verification_code(self, entered_code):
        valid_token = twilio.valid_verification_token(self.number, entered_code)
        if not valid_token:
            raise ValueError("validation is not valid")
        return True


class ReceivedMessage(BaseModel):
    id = models.AutoField(primary_key=True)
    twilio_message_id = models.CharField(max_length=34)
    data = JSONField()

    phone_number = models.ForeignKey(PhoneNumber, related_name="messages", on_delete=models.CASCADE)
