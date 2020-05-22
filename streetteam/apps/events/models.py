import logging
import uuid

from django_fsm import FSMField
from django.db import models

from apps.teams.models import Team
from common.models import BaseModel

logger = logging.getLogger(__name__)


class Event(BaseModel):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, null=False)
    team = models.ForeignKey(Team, related_name="events", on_delete=models.CASCADE, null=False)

    title = models.CharField(null=False, max_length=255)
    description = models.TextField(blank=True, null=False)
    happens_on = models.DateTimeField(null=False)

    # JSON log of all the things that happen to an event
    # a log is good enough for now; event source this
    # log = "" JSON field

    class EventStatus:
        """Status of event"""

        DRAFT = "draft"  # event has not yet been posted
        ACTIVE = "active"  # upcoming event
        INACTIVE = "inactive"  # upcoming event that is not being displayed
        DELETED = "deleted"  # deleted by user; can only delete upcoming events
        COMPLETED = "completed"  # event is done and can be see in archives

        CHOICES = [(DRAFT,) * 2, (ACTIVE,) * 2, (INACTIVE,) * 2, (DELETED,) * 2, (COMPLETED,) * 2]

        INITIAL_STATE = DRAFT

    event_status = FSMField(default=EventStatus.INITIAL_STATE, choices=EventStatus.CHOICES)
