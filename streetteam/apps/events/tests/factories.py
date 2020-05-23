from datetime import datetime, timedelta, timezone

import factory

from ..models import Event
from apps.teams.tests.factories import TeamFactory


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = Event

    title = "Chicago Python Presents"
    description = ""
    event_status = Event.EventStatus.DRAFT

    team = factory.SubFactory(TeamFactory)

    @factory.lazy_attribute
    def happens_on(self):
        return datetime.now(timezone.utc) + timedelta(weeks=1)
