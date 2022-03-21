import logging
import os
import uuid

from django.db import models
from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from imagekit.processors import Anchor, Thumbnail, Transpose

from .entities import MediaPost
from .managers import PostEventManager
from apps.twilio_integration.models import PhoneNumber
from apps.events.models import Event
from apps.users.models import User
from common.models import BaseModel

logger = logging.getLogger(__name__)


class MediaResource(BaseModel):
    id = models.AutoField(primary_key=True)
    resource_url = models.URLField(max_length=500)
    content_type = models.CharField(max_length=30, blank=True)

    phone_number = models.ForeignKey(PhoneNumber, related_name="media_resources", on_delete=models.CASCADE)


class ThumbnailSpec(ImageSpec):
    processors = [Transpose(), Thumbnail(height=500, width=500, anchor=Anchor.CENTER, crop=True, upscale=False)]
    format = "JPEG"
    options = {"quality": 60}


register.generator("mediahub:thumbnail", ThumbnailSpec)


def get_uploaded_images_path(self, filename):
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    path = os.path.join("uploaded-images", filename)
    return path


class UploadedImage(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    image = models.ImageField(upload_to=get_uploaded_images_path, null=False)
    thumbnail = ImageSpecField(source="image", id="mediahub:thumbnail")
    uploaded_by = models.ForeignKey(User, related_name="uploaded_images", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="images", on_delete=models.PROTECT, null=False)

    @property
    def caption(self):
        # TODO test
        events = self.events.get_log()
        caption = MediaPost(events).caption
        logger.info(caption)
        return caption


class PostEvent(BaseModel):
    """Represents all events associated with Media posts created by users

    TODO rename this to MediaPostEvent or ImagePostEvent
    """

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    image = models.ForeignKey(UploadedImage, related_name="events", on_delete=models.CASCADE)

    name = models.CharField(max_length=32, null=False)
    data = models.JSONField()

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

    @classmethod
    def create_caption_image_event(cls, user, image, caption):
        # TODO test this
        return cls(name="add_caption", performed_by=user, image=image, data={"caption": caption})
