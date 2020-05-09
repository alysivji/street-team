from .models import UploadedImage


def handle_uploaded_file(info):
    uploaded_image = UploadedImage(**info)
    uploaded_image.save()
