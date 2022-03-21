from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.DebugEndpoint.as_view()),
    path("authenticated/", view=views.AuthenticatedDebugEndpoint.as_view()),
    path("template/", view=views.DebugPageView.as_view(), name="template_view"),
]
