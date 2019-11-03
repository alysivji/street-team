from django.db import models
from ..twilio_integration.models import PhoneNumber


class MediaResource(models.Model):
    id = models.AutoField(primary_key=True)
    resource_url = models.URLField(max_length=500)
    content_type = models.CharField(max_length=30, blank=True)

    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
