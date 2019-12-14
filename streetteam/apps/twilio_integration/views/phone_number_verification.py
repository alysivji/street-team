from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import LinkPhoneNumberForm, ConfirmVerificationCodeForm
from ..models import PhoneNumber


@login_required
def enter_phone_number_to_send_verification_code(request):
    if request.method == "POST":
        form = LinkPhoneNumberForm(request.POST)
        if form.is_valid():
            validated_phone_number = form.cleaned_data["phone_number"]
            phone_number, _ = PhoneNumber.objects.get_or_create(number=validated_phone_number)
            phone_number.link_account(request.user)
            phone_number.save()

            # TODO flash a message that says we sent a code
            return HttpResponseRedirect(reverse("verify_code_send_via_sms"))
    else:
        form = LinkPhoneNumberForm()

    return render(request, "phone_number.html", {"form": form})


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
                # TODO FLASH: invalid code... try again
                return render(request, "enter_verification_code.html", {"form": form})

            phone_number.save()

            return HttpResponseRedirect(reverse("success"))
    else:
        form = ConfirmVerificationCodeForm()

    return render(request, "enter_verification_code.html", {"form": form})


@login_required
def success(request):
    return HttpResponse(b'{"status": "Success! Phone Number confirmed!"}', content_type="application/json")
