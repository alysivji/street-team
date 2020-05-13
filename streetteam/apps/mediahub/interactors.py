from io import BytesIO

from django.core.files.images import ImageFile
from PIL import Image

from .models import UploadedImage, PostEvent


def handle_uploaded_file(user, info):
    uploaded_image = UploadedImage(uploaded_by=user, **info)
    uploaded_image.save()

    upload_event = PostEvent.create_upload_event(user, uploaded_image)
    upload_event.save()


def crop_image(user, image_id, crop_box):
    image = Image.open(UploadedImage.objects.get(pk=image_id).image)

    cropped_blob = BytesIO()
    cropped_image = image.crop(crop_box)
    cropped_image.save(cropped_blob, image.format)
    my_img = ImageFile(name=f"temp.{image.format}", file=cropped_blob)

    instance = UploadedImage(user=user, image=my_img)
    instance.save()
    return my_img
