import pytest

from ..models import Event, is_future_event, is_past_event
from .factories import EventFactory


@pytest.mark.django_db
class TestEventModel:
    def test_create_and_retrieve_event(self):
        event = EventFactory(title="My event", description="Gonna be off the chain")

        record = Event.objects.first()

        assert record.title == event.title
        assert record.description == event.description
        assert record.event_status == Event.EventStatus.DRAFT


@pytest.mark.django_db
class TestEventStatustateMachine:
    def test_is_future_event__event_happens_tomorrow(self, ago):
        tomorrow = ago(days=-1)
        event = EventFactory(happens_on=tomorrow)
        assert is_future_event(event) is True

    @pytest.mark.freeze_time
    def test_is_future_event__event_happens_now(self, freezer, ago):
        now = ago()
        event = EventFactory(happens_on=now)
        assert is_future_event(event) is False

    def test_is_future_event__event_happened_yesterday(self, ago):
        yesterday = ago(days=1)
        event = EventFactory(happens_on=yesterday)
        assert is_future_event(event) is False

    def test_is_past_event__event_happens_tomorrow(self, ago):
        tomorrow = ago(days=-1)
        event = EventFactory(happens_on=tomorrow)
        assert is_past_event(event) is False

    @pytest.mark.freeze_time
    def test_is_past_event__event_happens_now(self, freezer, ago):
        now = ago()
        event = EventFactory(happens_on=now)
        assert is_past_event(event) is True

    def test_is_past_event__event_happened_yesterday(self, ago):
        yesterday = ago(days=1)
        event = EventFactory(happens_on=yesterday)
        assert is_past_event(event) is True
