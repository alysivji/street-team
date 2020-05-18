import datetime

import factory

from ..models import Event


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = Event

    title = "Chicago Python Presents"
    description = ""

    @factory.lazy_attribute
    def happens_on(self):
        return datetime.datetime.now() + datetime.timedelta(weeks=1)
