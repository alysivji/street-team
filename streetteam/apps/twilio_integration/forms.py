from django import forms


class LinkPhoneNumberForm(forms.Form):
    phone_number = forms.RegexField(
        label="Your phone number (xxx-xxx-xxxx format)",
        regex=r"^\d{3}[-\s]?\d{3}[-\s]?\d{4}$",
        error_messages={"invalid": "Phone number must be entered in the format: '555-555-5555'."},
    )


class ConfirmVerificationCodeForm(forms.Form):
    code = forms.CharField(label="Enter verification code", error_messages={"invalid": "Please enter code"})
