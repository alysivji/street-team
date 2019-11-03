from django.contrib.postgres.fields import JSONField
from django.db import models


class PhoneNumber(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.CharField(max_length=30)


class ReceivedMessage(models.Model):
    id = models.AutoField(primary_key=True)
    twilio_message_id = models.CharField(max_length=34)
    data = JSONField()

    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE)
