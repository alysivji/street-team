from django.urls import path
from .views import upload_file
from .views import crop_image_view, UploadedImagesDetailView, UploadedImagesListView

urlpatterns = [
    path("images/upload/", view=upload_file),
    path("images/", UploadedImagesListView.as_view(), name="images-list"),
    path("images/<int:pk>", UploadedImagesDetailView.as_view(), name="images-detail"),
    path("images/<str:uuid>/crop", crop_image_view, name="images-crop"),
]
