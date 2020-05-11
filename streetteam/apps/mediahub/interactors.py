from io import BytesIO

from django.core.files.images import ImageFile
from PIL import Image

from .models import CroppedImage, UploadedImage


def handle_uploaded_file(user, info):
    uploaded_image = UploadedImage(user=user, **info)
    uploaded_image.save()
    print(2)


def go_crop_image(user, image_id, crop_box):
    image = Image.open(UploadedImage.objects.get(pk=image_id).image)

    cropped_blob = BytesIO()
    cropped_image = image.crop(crop_box)
    cropped_image.save(cropped_blob, image.format)
    my_img = ImageFile(name=f"temp.{image.format}", file=cropped_blob)

    instance = CroppedImage(user=user, uploaded_image_id=image_id, image=my_img)
    instance.save()
    return True
