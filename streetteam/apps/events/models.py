import logging
import uuid

from django.db import models

from apps.teams.models import Team
from common.models import BaseModel

logger = logging.getLogger(__name__)


class TeamEvent(BaseModel):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, null=False)
    team = models.ForeignKey(Team, related_name="events", on_delete=models.CASCADE, null=False)

    title = models.CharField(null=False, max_length=255)
    description = models.TextField(blank=True, null=False)
    happens_on = models.DateTimeField(null=False)

    # TODO state machine for event_status field
    # Active
    # Inactive
    # Deleted (cannot have passed)
