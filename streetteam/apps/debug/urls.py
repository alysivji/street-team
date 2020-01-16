from django.urls import path
from .views import DebugEndpoint, DebugPageView

urlpatterns = [
    path("", view=DebugEndpoint.as_view()),
    path("template/", view=DebugPageView.as_view(), name="template_view"),
]
