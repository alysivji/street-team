from django.db import models

from apps.twilio_integration.models import PhoneNumber
from common.models import BaseModel


class MediaResource(BaseModel):
    id = models.AutoField(primary_key=True)
    resource_url = models.URLField(max_length=500)
    content_type = models.CharField(max_length=30, blank=True)

    phone_number = models.ForeignKey(PhoneNumber, related_name="media_resources", on_delete=models.CASCADE)


class Attachment(models.Model):
    file = models.FileField(upload_to="attachments")
