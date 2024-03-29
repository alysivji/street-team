"""streetteam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

urlpatterns = [
    # internal
    path("healthcheck/", lambda request: JsonResponse({"status": "healthy"})),
    path("debug/", include("apps.debug.urls"), name="debug"),
    # admin
    path("fubar/", admin.site.urls, name="admin"),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    # business functionality
    path("", include("apps.mediahub.urls"), name="mediahub"),
    path("", include("apps.events.urls"), name="events"),
    path("", include("apps.teams.urls"), name="teams"),
    path("", include("apps.website.urls"), name="website"),
    path("sms/", include("apps.twilio_integration.urls"), name="twilio_integration"),
    # third party apps
    path("watchman/", include("watchman.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = "ChiPy Street Team Administration"
admin.site.site_title = "ChiPy Street Team Administration"
