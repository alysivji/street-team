from .models import Event


def create_event(user, team, event_information):
    event = Event(team=team, **event_information)
    event.save()

    # TODO do not save full event first time
    # or just save it again to capture in log
    # event.log.append({"action": "create_event", "user_id": user.id})
    # event.save()
