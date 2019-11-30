from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ("email",)


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)


class LinkPhoneNumberForm(forms.Form):
    phone_number = forms.RegexField(
        label="Your phone number (xxx-xxx-xxxx format)",
        regex=r"^\d{3}[-\s]?\d{3}[-\s]?\d{4}$",
        error_messages={"invalid": "Phone number must be entered in the format: '555-555-5555'."},
    )


class ConfirmVerificationCodeForm(forms.Form):
    code = forms.CharField(label="Enter verification code", error_messages={"invalid": "Please enter code"})
