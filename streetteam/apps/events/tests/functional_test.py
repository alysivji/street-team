from datetime import datetime, timedelta, timezone

import pytest

from apps.teams.models import UserTeamMembership
from apps.teams.tests.factories import UserTeamMembershipFactory


@pytest.mark.django_db
@pytest.mark.end2end
class TestCreatingEventWorkflow:
    @pytest.mark.current
    def test_create_new_event__happy_path(self, client, login_user):
        # Arrange
        admin_membership = UserTeamMembershipFactory(position_state=UserTeamMembership.PositionState.ADMIN)
        user = admin_membership.user
        team = admin_membership.team
        login_user(user)

        tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

        # Act
        form_data = {
            "title": "Event",
            "description": "My Description",
            "happens_on": tomorrow.strftime("%Y-%m-%d %H:%M"),
        }
        resp = client.post(f"/teams/{team.uuid}/events/new", form_data)

        # check that user is on team
        assert resp.status_code == 302
