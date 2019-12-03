from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..adapter import twilio
from ..forms import LinkPhoneNumberForm, ConfirmVerificationCodeForm
from ..models import PhoneNumber


@login_required
def enter_phone_number_to_send_verification_code(request):
    if request.method == "POST":
        form = LinkPhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number_str = form.cleaned_data["phone_number"]
            validated_phone_number = validate_phone_number(phone_number_str)
            phone_number, _ = PhoneNumber.objects.get_or_create(number=validated_phone_number)
            phone_number.link_account(request.user)
            phone_number.save()

            # TODO flash a message that says we sent a code
            return HttpResponseRedirect(reverse("verify_code_send_via_sms"))
    else:
        form = LinkPhoneNumberForm()

    return render(request, "phone_number.html", {"form": form})


def validate_phone_number(phone_number):
    """Validate with Twilio and return E.164 format that is tored in DB"""
    phone_number = twilio.verify_phone_number(phone_number)
    if not phone_number.is_valid:
        raise ValidationError("Not a valid phone number")
    if phone_number.country_code not in ["US"]:
        raise ValidationError("Curently only accepting US numbers")

    return phone_number.number


@login_required
def verify_code_send_via_sms(request):
    if request.method == "POST":
        form = ConfirmVerificationCodeForm(request.POST)
        if form.is_valid():
            user = request.user
            phone_number: PhoneNumber = user.phone_numbers.all()[0]

            try:
                phone_number.confirm_verification_code(form.cleaned_data["code"])
            except ValueError:
                raise ValidationError("Invalid code. Please try again.")

            phone_number.save()

            return HttpResponseRedirect(reverse("success"))
    else:
        form = ConfirmVerificationCodeForm()

    return render(request, "enter_verification_code.html", {"form": form})


@login_required
def success(request):
    return HttpResponse(b'{"status": "Success! Phone Number confirmed!"}', content_type="application/json")
