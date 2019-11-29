import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# from django_fsm import FSMField, transition

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    email = models.EmailField(_("email address"), unique=True)
    username = models.EmailField(null=True)  # field is required for python social auth

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    # # Account Creation State Machine
    # class STATE:
    #     ACCOUNT_CREATED = "account_created"
    #     ATTEMPT_PHONE_LINK = "attempt_phone_link"
    #     PHONE_LINK_SUCCESS = "phone_link_success"
    #     PHONE_LINK_FAILED = "phone_link_failed"

    # STATE_CHOICES = [
    #     (STATE.ACCOUNT_CREATED, "account_created", "account_created"),
    #     (STATE.ATTEMPT_PHONE_LINK, "attempt_phone_link", "attempt_phone_link"),
    #     (STATE.PHONE_LINK_SUCCESS, "phone_link_success", "phone_link_success"),
    #     (STATE.PHONE_LINK_FAILED, "phone_link_failed", "phone_link_failed"),
    # ]

    # state = FSMField(default=STATE.ACCOUNT_CREATED, state_choices=STATE_CHOICES)

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
