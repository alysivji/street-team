from django.db import models

from .entities import EVENTS_LIST


class PostEventManager(models.Manager):
    def get_log(self):
        events = []
        for event in self.order_by("id").all():
            for EventClass in EVENTS_LIST:
                my_event = event.to_dict()
                if EventClass.match(my_event):
                    events.append(EventClass(**my_event["details"]))
        return events
