import logging
from django.db import models
from common.models import BaseModel

logger = logging.getLogger(__name__)


class TeamEvent(BaseModel):
    id = models.AutoField(primary_key=True)

    title = models.CharField(null=False, max_length=255)
    description = models.TextField(blank=True, null=False)
    happens_on = models.DateTimeField(null=False)

    # TODO foreign key with teams
    # TODO state machine for event_status field
    # Active
    # Inactive
