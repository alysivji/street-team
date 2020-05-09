import os
import uuid

from django.db import models

from apps.twilio_integration.models import PhoneNumber
from apps.users.models import User
from common.models import BaseModel


def get_file_path(self, filename):
    # all files are saved in streetteam/chicago-python
    # this is hacked together right now
    # fix later
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    path = os.path.join("uploaded-images", filename)
    return path


class MediaResource(BaseModel):
    id = models.AutoField(primary_key=True)
    resource_url = models.URLField(max_length=500)
    content_type = models.CharField(max_length=30, blank=True)

    phone_number = models.ForeignKey(PhoneNumber, related_name="media_resources", on_delete=models.CASCADE)


class UploadedImage(models.Model):
    image = models.ImageField(upload_to=get_file_path, null=True, blank=True)
    user = models.ForeignKey(User, related_name="uploaded_images", on_delete=models.CASCADE)
