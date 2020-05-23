from datetime import datetime, timezone, timedelta

from dateutil.relativedelta import relativedelta
import pytest

from ..models import Event
from apps.teams.models import UserTeamMembership
from apps.teams.tests.factories import UserTeamMembershipFactory


@pytest.mark.django_db
@pytest.mark.end2end
class TestCreatingEventWorkflow:
    def test_create_new_event__happy_path(self, client, login_user):
        # Arrange
        admin_membership = UserTeamMembershipFactory(position_state=UserTeamMembership.PositionState.ADMIN)
        user = admin_membership.user
        team = admin_membership.team
        login_user(user)

        tomorrow = datetime.now(timezone.utc) + relativedelta(days=1)

        # Act
        form_data = {
            "title": "Event",
            "description": "My Description",
            "happens_on": tomorrow.strftime("%Y-%m-%d %H:%M:%S"),
        }
        resp = client.post(f"/teams/{team.uuid}/events/new", form_data)

        # Assert event has been created
        assert resp.status_code == 302
        event = Event.objects.first()
        assert event.team == team
        assert event.title == "Event"
        assert event.description == "My Description"
        assert abs(event.happens_on - tomorrow) <= timedelta(seconds=1)

    def test_create_new_event__cannot_create_event_in_past(self, client, login_user):
        # Arrange
        admin_membership = UserTeamMembershipFactory(position_state=UserTeamMembership.PositionState.ADMIN)
        user = admin_membership.user
        team = admin_membership.team
        login_user(user)

        yesterday = datetime.now(timezone.utc) - relativedelta(days=1)

        # Act
        form_data = {
            "title": "Event",
            "description": "My Description",
            "happens_on": yesterday.strftime("%Y-%m-%d %H:%M"),
        }
        resp = client.post(f"/teams/{team.uuid}/events/new", form_data)

        # Assert event has not been created
        assert resp.status_code == 200
        assert Event.objects.count() == 0
