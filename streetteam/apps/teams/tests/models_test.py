import pytest

from ..models import UserTeam, user_is_only_member_of_team, user_has_position_state_requested
from .factories import UserTeamMembershipFactory
from apps.users.tests.factories import UserFactory


##############################################
# User to Team many-to-many relationship tests
##############################################
@pytest.mark.django_db
def test_user_is_only_member_of_team__happy_path():
    member = UserTeamMembershipFactory()
    assert user_is_only_member_of_team(member)


@pytest.mark.django_db
def test_user_is_only_member_of_team__group_has_two_members():
    first_member = UserTeamMembershipFactory(user=UserFactory())
    second_member = UserTeamMembershipFactory(user=UserFactory(), team=first_member.team)
    assert not user_is_only_member_of_team(second_member)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "position_state, expected_result",
    [
        (UserTeam.PositionState.REQUESTED, True),
        (UserTeam.PositionState.REJECTED, False),
        (UserTeam.PositionState.WITHDREW, False),
        (UserTeam.PositionState.RELEASED, False),
        (UserTeam.PositionState.MEMBER, False),
        (UserTeam.PositionState.TEAM_LEAD, False),
        (UserTeam.PositionState.ORGANIZER, False),
        (UserTeam.PositionState.ADMIN, False),
    ],
)
def test_user_has_position_member(position_state, expected_result):
    member = UserTeamMembershipFactory(user=UserFactory(), position_state=position_state)
    assert user_has_position_state_requested(member) is expected_result


@pytest.mark.django_db
# TODO test this using freeze gun
def test_team_was_just_created__happy_path():
    pass
