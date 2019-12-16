from django.urls import path
from .views import AccountView, IndexView

urlpatterns = [path("", view=IndexView.as_view()), path("account/", view=AccountView.as_view())]
