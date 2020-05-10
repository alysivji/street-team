from django.urls import path
from .views import upload_file
from .views import UploadedImagesDetailView, UploadedImagesListView

urlpatterns = [
    path("upload/", view=upload_file),
    path("images/", UploadedImagesListView.as_view(), name="images-list"),
    path("images/<int:pk>", UploadedImagesDetailView.as_view(), name="images-detail"),
]
