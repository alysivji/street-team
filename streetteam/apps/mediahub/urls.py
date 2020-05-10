from django.urls import path
from .views import upload_file
from .views import UploadedImagesListView

urlpatterns = [path("upload/", view=upload_file), path("", UploadedImagesListView.as_view(), name="article-list")]
