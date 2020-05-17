import datetime

import factory

from ..models import Event


class EventFactory(factory.DjangoModelFactory):
    class Meta:
        model = Event

    title = "Chicago Python Presents"
    description = ""

    @factory.lazy_attribute
    def happened_at(self):
        return datetime.datetime.now() + datetime.timedelta(weeks=1)
