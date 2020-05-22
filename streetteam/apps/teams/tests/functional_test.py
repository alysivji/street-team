import pytest

from .factories import TeamFactory
from ..models import UserTeamMembership

from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.end2end
class TestUserJoiningTeamWorkflow:
    @pytest.mark.current
    def test_user_joins_team__happy_path(self, client, login_user):
        # Arrange
        team = TeamFactory()
        user = UserFactory()
        login_user(user)

        # user enters join code successfully; use the view
        resp = client.post(f"/teams/join/", data={"uuid": team.join_code})

        # check that user is on team
        assert resp.status_code == 302
        conditions = {"team": team, "user": user}
        membership = UserTeamMembership.objects.filter(**conditions).all()
        assert len(membership) == 1
