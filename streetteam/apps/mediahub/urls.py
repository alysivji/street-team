from django.urls import path
from .views import upload_file
from .views import crop_image_view, UploadedImagesDetailView, UploadedImagesListView

urlpatterns = [
    path("images/upload/", view=upload_file, name="images-upload"),
    path("images/", UploadedImagesListView.as_view(), name="images-list"),
    path("images/<str:uuid>", UploadedImagesDetailView.as_view(), name="images-detail"),
    path("images/<str:uuid>/crop", crop_image_view, name="images-crop"),
]
