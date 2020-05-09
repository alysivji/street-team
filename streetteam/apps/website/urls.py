from django.urls import path
from .views import AccountView, IndexView, upload_file

urlpatterns = [
    path("", view=IndexView.as_view()),
    path("account/", view=AccountView.as_view()),
    path("upload/", view=upload_file),
]
