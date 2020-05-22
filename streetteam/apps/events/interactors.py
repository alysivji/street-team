from .models import Event


def create_event(user, team, event_information):
    event = Event(team=team, **event_information)
    event.save()

    event.log.append({"action": "create_event", "user_id": user.id})
    event.save()
