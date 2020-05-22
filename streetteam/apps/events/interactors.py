from .models import Event


def create_event(user, team, event_information):
    event = Event(team=team, **event_information)
    event.save()

    # todo json log
    # add who created it
