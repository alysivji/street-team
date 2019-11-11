from django.contrib.postgres.fields import JSONField
from django.db import models
from apps.common.models import BaseModel


class PhoneNumber(BaseModel):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=30, unique=True)


class ReceivedMessage(BaseModel):
    id = models.AutoField(primary_key=True)
    twilio_message_id = models.CharField(max_length=34)
    data = JSONField()

    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
