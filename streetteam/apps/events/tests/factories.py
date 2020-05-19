from datetime import datetime, timedelta, timezone

import factory

from ..models import TeamEvent
from apps.teams.tests.factories import TeamFactory


class TeamEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = TeamEvent

    title = "Chicago Python Presents"
    description = ""

    team = factory.SubFactory(TeamFactory)

    @factory.lazy_attribute
    def happens_on(self):
        return datetime.now(timezone.utc) + timedelta(weeks=1)
