from django_fsm import TransitionNotAllowed
import pytest

from .factories import TeamFactory
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
    assert membership.position_state == UserTeam.PositionState.ADMIN


def test_make_user_admin_of_team__transition_not_allowed():
    # TODO
    with pytest.raises(TransitionNotAllowed):
        pass
