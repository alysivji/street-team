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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.urls import include, path

from apps.common.views import DebugEndpoint

urlpatterns = [
    path("admin/", admin.site.urls),
    path("integration/", include("apps.twilio_integration.urls")),
    path(
        "healthcheck/",
        lambda request: HttpResponse(
            b'{"ping": "pong"}', content_type="application/json"
        ),
    ),
    path("debug/", view=DebugEndpoint.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
