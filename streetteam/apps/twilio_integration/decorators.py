import functools

from django.http import HttpResponseForbidden
from twilio.request_validator import RequestValidator


def validate_twilio_request(signing_secret: str):

    if not isinstance(signing_secret, str):
        raise ValueError
    validator = RequestValidator(signing_secret)

    def verification_decorator(func):
        @functools.wraps(func)
        def decorated_function(request, *args, **kwargs):
            request_valid = validator.validate(
                request.build_absolute_uri(),
                request.POST,
                request.META.get("HTTP_X_TWILIO_SIGNATURE", ""),
            )

            if request_valid:
                return func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden()

        return decorated_function

    return verification_decorator
