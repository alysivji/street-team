import logging
from django.db import models
from common.models import BaseModel

logger = logging.getLogger(__name__)


class Event(BaseModel):
    """Rename this to TeamEvent"""

    id = models.AutoField(primary_key=True)

    title = models.CharField(null=False, max_length=255)
    description = models.TextField(blank=True, null=False)
    happened_at = models.DateTimeField(null=False)
    # TODO make this happens_on

    # TODO foreign key with teams
    # TODO state machine for event_status field
    # Active
    # Inactive
