from django.conf import settings


def from_settings(request):
    return {
        "ENVIRONMENT_NAME": "Production" if settings.IN_PRODUCTION else "Development",
        "ENVIRONMENT_COLOR": "red" if settings.IN_PRODUCTION else "grey",
    }
