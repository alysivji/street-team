import pytest

from ..models import (
    can_perform_group_modifications,
    is_admin,
    user_has_position_state_requested,
    user_is_only_member_of_team,
    UserTeam,
)
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
def test_user_has_position_state_requested(position_state, expected_result):
    membership = UserTeamMembershipFactory(user=UserFactory(), position_state=position_state)
    assert user_has_position_state_requested(membership) is expected_result


@pytest.mark.django_db
# TODO test this using freeze gun
def test_team_was_just_created__happy_path():
    # test created 59 seconds ago
    # test created 60 seconds ago
    # test created 61 seconds ago
    pass


@pytest.mark.django_db
@pytest.mark.parametrize(
    "position_state, expected_result",
    [
        (UserTeam.PositionState.REQUESTED, False),
        (UserTeam.PositionState.REJECTED, False),
        (UserTeam.PositionState.WITHDREW, False),
        (UserTeam.PositionState.RELEASED, False),
        (UserTeam.PositionState.MEMBER, False),
        (UserTeam.PositionState.TEAM_LEAD, False),
        (UserTeam.PositionState.ORGANIZER, True),
        (UserTeam.PositionState.ADMIN, True),
    ],
)
def test_can_perform_group_modifications(position_state, expected_result):
    user = UserFactory()
    membership = UserTeamMembershipFactory(user=user, position_state=position_state)
    assert can_perform_group_modifications(membership, user) is expected_result


@pytest.mark.django_db
@pytest.mark.parametrize(
    "position_state, expected_result",
    [
        (UserTeam.PositionState.REQUESTED, False),
        (UserTeam.PositionState.REJECTED, False),
        (UserTeam.PositionState.WITHDREW, False),
        (UserTeam.PositionState.RELEASED, False),
        (UserTeam.PositionState.MEMBER, False),
        (UserTeam.PositionState.TEAM_LEAD, False),
        (UserTeam.PositionState.ORGANIZER, False),
        (UserTeam.PositionState.ADMIN, True),
    ],
)
def test_is_admin(position_state, expected_result):
    user = UserFactory()
    membership = UserTeamMembershipFactory(user=user, position_state=position_state)
    assert is_admin(membership, user) is expected_result
