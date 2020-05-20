from django_fsm import TransitionNotAllowed
import pytest

from .factories import TeamFactory, UserTeamMembershipFactory
from ..interactors import make_user_admin_of_team
from ..models import UserTeamMembership
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_make_user_admin_of_team__happy_path():
    # Arrange
    team = TeamFactory()
    user = UserFactory()

    # Act
    make_user_admin_of_team(user, team)

    # Assert
    membership = UserTeamMembership.objects.first()
    assert membership.team == team
    assert membership.user == user
    assert membership.position_state == UserTeamMembership.PositionState.ADMIN


@pytest.mark.django_db
def test_make_user_admin_of_team__transition_not_allowed():
    # Arrange
    membership = UserTeamMembershipFactory()
    user = UserFactory()

    # Act / Assert
    with pytest.raises(TransitionNotAllowed):
        make_user_admin_of_team(user, team=membership.team)
