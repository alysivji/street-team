import os
import uuid

from django.db import models

from apps.twilio_integration.models import PhoneNumber
from apps.users.models import User
from common.models import BaseModel


class MediaResource(BaseModel):
    id = models.AutoField(primary_key=True)
    resource_url = models.URLField(max_length=500)
    content_type = models.CharField(max_length=30, blank=True)

    phone_number = models.ForeignKey(PhoneNumber, related_name="media_resources", on_delete=models.CASCADE)


def get_uploaded_images_path(self, filename):
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    path = os.path.join("uploaded-images", filename)
    return path


class UploadedImage(BaseModel):
    image = models.ImageField(upload_to=get_uploaded_images_path)
    user = models.ForeignKey(User, related_name="uploaded_images", on_delete=models.CASCADE)


def get_cropped_images_path(self, filename):
    import pdb

    pdb.set_trace()
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    path = os.path.join("cropped-images", filename)
    return path


class CroppedImage(BaseModel):
    image = models.ImageField(upload_to=get_cropped_images_path, null=False, blank=False)
    user = models.ForeignKey(User, related_name="cropped_images", on_delete=models.CASCADE)
    uploaded_image = models.ForeignKey(UploadedImage, related_name="cropped_images", on_delete=models.CASCADE)
