from django.contrib.postgres.fields import JSONField
from django.db import models
from django_fsm import FSMField  # transition

from apps.common.models import BaseModel


class PhoneNumber(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=30, unique=True)

    class STATE:
        """Has phone_number been linked to account"""

        UNLINKED_PHONE_NUMBER = "unlinked_phone_number"
        ATTEMPT_PHONE_LINK = "attempt_phone_link"
        PHONE_LINK_SUCCESS = "phone_link_success"
        PHONE_LINK_FAILED = "phone_link_failed"

    STATE_CHOICES = [
        (STATE.UNLINKED_PHONE_NUMBER,) * 3,
        (STATE.ATTEMPT_PHONE_LINK,) * 3,
        (STATE.PHONE_LINK_SUCCESS,) * 3,
        (STATE.PHONE_LINK_FAILED,) * 3,
    ]

    account_link_state = FSMField(default=STATE.UNLINKED_PHONE_NUMBER, state_choices=STATE_CHOICES)

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
