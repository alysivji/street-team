import pytest

from ..models import Event
from .factories import EventFactory


@pytest.mark.django_db
def test_create_and_retrieve_event():
    event = EventFactory(title="My event", description="Gonna be off the chain")

    record = Event.objects.first()

    assert record.title == event.title
    assert record.description == event.description
