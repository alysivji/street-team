from django_fsm import TransitionNotAllowed
import pytest

from .factories import TeamFactory, UserTeamMembershipFactory
from ..interactors import make_user_admin_of_team
from ..models import UserTeam
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
def test_make_user_admin_of_team__happy_path():
    team = TeamFactory()
    user = UserFactory()

    make_user_admin_of_team(user, team)

    membership = UserTeam.objects.first()
    assert membership.team == team
    assert membership.user == user
    assert membership.position == UserTeam.PositionState.ADMIN


@pytest.mark.django_db
def test_make_user_admin_of_team__transition_not_allowed():
    membership = UserTeamMembershipFactory()
    user = UserFactory()

    with pytest.raises(TransitionNotAllowed):
        make_user_admin_of_team(user, team=membership.team)
