import os
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from .managers import PostEventManager
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
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    image = models.ImageField(upload_to=get_uploaded_images_path, null=False)
    uploaded_by = models.ForeignKey(User, related_name="uploaded_images", on_delete=models.CASCADE)


class PostEvent(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    image = models.ForeignKey(UploadedImage, related_name="events", on_delete=models.CASCADE)

    name = models.CharField(max_length=32, null=False)
    data = JSONField()

    performed_by = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)

    objects = PostEventManager()

    def to_dict(self):
        return {"uuid": self.uuid, "type": self.name, "details": self.data}

    @classmethod
    def create_upload_event(cls, user, image):
        return cls(name="upload_image", performed_by=user, image=image, data={})

    @classmethod
    def create_crop_image_event(cls, user, image, crop_box):
        return cls(name="crop_image", performed_by=user, image=image, data=crop_box)
