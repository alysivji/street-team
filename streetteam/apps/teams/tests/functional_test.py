import pytest

from .factories import TeamFactory
from ..models import UserTeamMembership

from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
@pytest.mark.end2end
class TestUserJoiningTeamWorkflow:
    def test_user_joins_team__happy_path(self, client, login_user):
        # Arrange
        team = TeamFactory()
        user = UserFactory()
        login_user(user)

        # Act
        resp = client.post(f"/teams/join/", {"join_code": team.join_code})

        # check that user is on team
        assert resp.status_code == 302
        conditions = {"team": team, "user": user}
        membership = UserTeamMembership.objects.filter(**conditions).all()
        assert len(membership) == 1

    def test_user_joins_team_with_old_join_code__rejected(self, client, login_user):
        # Arrange
        team = TeamFactory()
        old_join_code = team.join_code
        team.generate_new_join_code()
        user = UserFactory()
        login_user(user)

        # Act
        resp = client.post(f"/teams/join/", {"join_code": old_join_code})

        # Assert user should not be on team
        assert resp.status_code == 200
        conditions = {"team": team, "user": user}
        membership = UserTeamMembership.objects.filter(**conditions).all()
        assert len(membership) == 0
