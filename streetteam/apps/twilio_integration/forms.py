from django import forms
from django.core.exceptions import ValidationError

from .adapter import twilio
from .exceptions import PhoneNumberNotValid


class LinkPhoneNumberForm(forms.Form):
    phone_number = forms.RegexField(
        label="Your phone number (xxx-xxx-xxxx format)",
        regex=r"^\d{3}[-\s]?\d{3}[-\s]?\d{4}$",
        error_messages={"invalid": "Phone number must be entered in the format: '555-555-5555'."},
    )

    def clean_phone_number(self):
        """If valid, returns phone_number in E.164 format"""
        number = self.cleaned_data.get("phone_number")

        try:
            phone_number = twilio.verify_phone_number(number)
        except PhoneNumberNotValid:
            raise ValidationError("Not a valid phone number")

        if phone_number.country_code not in ["US"]:
            raise ValidationError("Curently only accepting US numbers")

        return phone_number.number


class ConfirmVerificationCodeForm(forms.Form):
    code = forms.CharField(label="Enter verification code", error_messages={"invalid": "Please enter code"})
