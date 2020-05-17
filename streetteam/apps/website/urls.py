from django.urls import path
from .views import AccountView, IndexView, logout_view

urlpatterns = [
    path("", view=IndexView.as_view(), name="index"),
    path("account/", view=AccountView.as_view(), name="account-details"),
    path("logout/", view=logout_view, name="logout"),
]
