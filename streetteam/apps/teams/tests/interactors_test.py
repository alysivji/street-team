from django_fsm import TransitionNotAllowed
from django_fsm_log.models import StateLog
import pytest

from .factories import TeamFactory, UserTeamMembershipFactory
from ..interactors import make_user_admin_of_team
from ..models import UserTeam
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_make_user_admin_of_team__happy_path():
    # Arrange
    team = TeamFactory()
    user = UserFactory()

    # Act
    make_user_admin_of_team(user, team)

    # Assert
    membership = UserTeam.objects.first()
    assert membership.team == team
    assert membership.user == user
    assert membership.position == UserTeam.PositionState.ADMIN

    # not sure if i actually need to test this
    logs = StateLog.objects.all()
    assert len(logs) == 1
    log = logs[0]
    assert log.by == user
    assert log.source_state == UserTeam.PositionState.MEMBER
    assert log.state == UserTeam.PositionState.ADMIN
    assert log.transition == "make_user_admin_of_newly_created_group"


@pytest.mark.django_db
def test_make_user_admin_of_team__transition_not_allowed():
    # Arrange
    membership = UserTeamMembershipFactory()
    user = UserFactory()

    # Act / Assert
    with pytest.raises(TransitionNotAllowed):
        make_user_admin_of_team(user, team=membership.team)
