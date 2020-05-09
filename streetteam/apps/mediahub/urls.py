from django.urls import path
from .views import upload_file

urlpatterns = [path("upload/", view=upload_file)]
