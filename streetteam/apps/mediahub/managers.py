from django.db import models

from .entities import EVENTS_LIST


class PostEventManager(models.Manager):
    def get_log(self):
        events = []
        for event in self.order_by("id").all():
            event_dict = event.to_dict()
            for EventClass in EVENTS_LIST:
                if EventClass.match(event_dict):
                    events.append(EventClass(**event_dict["details"]))
        return events
