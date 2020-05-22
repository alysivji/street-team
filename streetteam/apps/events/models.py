from datetime import datetime, timezone
import logging
import uuid

from django_fsm import FSMField, transition
from django_fsm_log.decorators import fsm_log_by
from django.db import models

from apps.teams.models import Team
from common.models import BaseModel

logger = logging.getLogger(__name__)


def is_future_event(instance):
    now = datetime.now(timezone.utc)
    if instance.happens_on > now:
        return True
    return False


def is_past_event(instance):
    return not is_future_event(instance)


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

    @fsm_log_by
    @transition(field=event_status, source=EventStatus.DRAFT, target=EventStatus.DRAFT)
    def update_draft(self, by):
        pass

    @fsm_log_by
    @transition(field=event_status, source=EventStatus.DRAFT, target=EventStatus.ACTIVE, conditions=[is_future_event])
    def publish(self, by):
        pass

    @fsm_log_by
    @transition(field=event_status, source=EventStatus.ACTIVE, target=EventStatus.INACTIVE)
    def hide(self, by):
        pass

    @fsm_log_by
    @transition(
        field=event_status, source=EventStatus.INACTIVE, target=EventStatus.ACTIVE, conditions=[is_future_event]
    )
    def unhide(self, by):
        pass

    @fsm_log_by
    @transition(
        field=event_status,
        source=[EventStatus.DRAFT, EventStatus.ACTIVE, EventStatus.INACTIVE],
        target=EventStatus.DELETED,
        conditions=[is_future_event],
    )
    def delete(self, by):
        pass

    @fsm_log_by
    @transition(field=event_status, source=EventStatus.ACTIVE, target=EventStatus.COMPLETED, conditions=[is_past_event])
    def archive(self, by):
        """Should this be a user action or a CRON job if the event is over a few days old"""
        pass
