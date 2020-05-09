import os
import uuid

from django.db import models

from apps.twilio_integration.models import PhoneNumber
from common.models import BaseModel
from common.storage import MediaStorage


def get_file_path(self, filename):
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    # TODO change when we become multitenant
    return os.path.join(MediaStorage.location, "uploaded-images", filename)


class MediaResource(BaseModel):
    id = models.AutoField(primary_key=True)
    resource_url = models.URLField(max_length=500)
    content_type = models.CharField(max_length=30, blank=True)

    phone_number = models.ForeignKey(PhoneNumber, related_name="media_resources", on_delete=models.CASCADE)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
