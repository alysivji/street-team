from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms import LinkPhoneNumberForm, ConfirmVerificationCodeForm


# TODO Requires auth
def enter_phone_number_to_send_verification_code(request):
    if request.method == "POST":
        form = LinkPhoneNumberForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("verify_code_send_via_sms"))
    else:
        form = LinkPhoneNumberForm()

    return render(request, "phone_number.html", {"form": form})


# TODO Requires auth
def verify_code_send_via_sms(request):
    if request.method == "POST":
        form = ConfirmVerificationCodeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("success"))
    else:
        form = ConfirmVerificationCodeForm()

    return render(request, "enter_verification_code.html", {"form": form})


# TODO Requires auth
def success(request):
    return HttpResponse(b'{"ping": "pong"}', content_type="application/json")
