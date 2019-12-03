from django.contrib.postgres.fields import JSONField
from django.db import models
from django_fsm import FSMField  # transition

from apps.common.models import BaseModel


class PhoneNumber(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=30, unique=True)

    # Account Creation State Machine
    class STATE:
        NO_ACCOUNT = "no_account"
        ACCOUNT_CREATED = "account_created"
        ATTEMPT_PHONE_LINK = "attempt_phone_link"
        PHONE_LINK_SUCCESS = "phone_link_success"
        PHONE_LINK_FAILED = "phone_link_failed"

    STATE_CHOICES = [
        (STATE.NO_ACCOUNT, "no_account", "no_account"),
        (STATE.ACCOUNT_CREATED, "account_created", "account_created"),
        (STATE.ATTEMPT_PHONE_LINK, "attempt_phone_link", "attempt_phone_link"),
        (STATE.PHONE_LINK_SUCCESS, "phone_link_success", "phone_link_success"),
        (STATE.PHONE_LINK_FAILED, "phone_link_failed", "phone_link_failed"),
    ]

    account_creation_status = FSMField(default=STATE.NO_ACCOUNT, state_choices=STATE_CHOICES)

    # TODO save should also have a transition
    # override SAVE ala 2 scoops

    # @transition(field=state, source=STATE.ACCOUNT_CREATED, target=state.ATTEMPT_PHONE_LINK)
    # def link_phone_number(self):
    #     # ask them to enter a phone number, use Twilio API to ensure number is valid
    #     # send a text message to that number with code, store code in database
    #     pass

    # @transition(
    #     field=state, source=STATE.ATTEMPT_PHONE_LINK, target=state.PHONE_LINK_SUCCESS,
    # on_error=STATE.PHONE_LINK_FAILED
    # )
    # def phone_successfully_linked(self, entered_code):
    #     pass

    # @transition(field=state, source=STATE.PHONE_LINK_FAILED, target=STATE.ATTEMPT_PHONE_LINK)
    # def retry_link_phone_number(self):
    #     pass


class ReceivedMessage(BaseModel):
    id = models.AutoField(primary_key=True)
    twilio_message_id = models.CharField(max_length=34)
    data = JSONField()

    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
