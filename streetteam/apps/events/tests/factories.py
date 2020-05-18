import datetime

import factory

from ..models import TeamEvent


class TeamEventFactory(factory.DjangoModelFactory):
    class Meta:
        model = TeamEvent

    title = "Chicago Python Presents"
    description = ""

    @factory.lazy_attribute
    def happens_on(self):
        return datetime.datetime.now() + datetime.timedelta(weeks=1)
