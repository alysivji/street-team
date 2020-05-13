from .forms import CropBox
from .models import UploadedImage, PostEvent


def handle_uploaded_file(user, info):
    uploaded_image = UploadedImage(uploaded_by=user, **info)
    uploaded_image.save()

    upload_event = PostEvent.create_upload_event(user, uploaded_image)
    upload_event.save()


def crop_image(user, image, cropbox: CropBox):
    crop_event = PostEvent.create_crop_image_event(user, image=image, cropbox=cropbox.to_dict())
    crop_event.save()
