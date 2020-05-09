from .models import UploadedImage


def handle_uploaded_file(user, info):
    uploaded_image = UploadedImage(user=user, **info)
    uploaded_image.save()
    print(2)
